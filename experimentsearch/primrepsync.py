from mongcore import document_change_listener
from mongcore.document_change_listener import ChangeLog, Addition, Deletion, Update
from kaka.settings import PRIMARY_DB_ALIAS
from mongoengine.context_managers import switch_db
from bson.objectid import ObjectId


def synchronise():
    """
    Ensures that the docs in both the primary and local db match.

    Checks for any ChangeLog documents not in both the primary and the
    replica's change_log collection, then adds those documents to the database they
    were missing from.
    Once ChangeLogs are synced, orders the ChangeLogs by time. Starting from the
    ChangeLog that was previously not in both databases with the earliest date,
    iterates through the ChangeLogs applying and reapplying the changes represented
    by the ChangeLogs to both databases. This ensures the other collections of both
    databases match

    :return:
    """
    # Turns off change logging while syncing
    document_change_listener.logging = False

    # Finds the ChangeLogs unique to the primary, using UUIDs
    rep_changes = ChangeLog.objects.all()
    change_uuids = rep_changes.scalar('uuid')
    with switch_db(ChangeLog, PRIMARY_DB_ALIAS) as Prim:
        prim_change_uuids = Prim.objects.all().scalar('uuid')
        prim_changes = Prim.objects(uuid__nin=change_uuids)

    # finds the ChangeLogs unique to the replica, using UUIDs
    unique_rep_changes = ChangeLog.objects(uuid__nin=prim_change_uuids)

    if len(prim_changes) == 0 and len(unique_rep_changes) == 0:
        return  # No new changes to either database

    earliest = earliest_unique_change_time(prim_changes, unique_rep_changes)

    # Applies and reapplies the changes from both databases to both
    # databases, starting from the earliest unique change
    all_changes = rep_changes.insert(prim_changes)
    make_changes = all_changes.filter(time__gte=earliest)
    make_changes = make_changes.order_by("+time")
    for change in make_changes:
        apply_change(change)
        apply_change(change, db_alias=PRIMARY_DB_ALIAS)

    # Switch change logging back on
    document_change_listener.logging = True


def earliest_unique_change_time(prim_changes, unique_rep_changes):
    # finds the earliest ChangeLog's time unique to either database
    unique_rep_changes = unique_rep_changes.order_by("+time")
    prim_changes = prim_changes.order_by("+time")
    if len(prim_changes) == 0:
        return unique_rep_changes[0].time
    if len(unique_rep_changes) == 0:
        return prim_changes[0].time
    return min(prim_changes[0].time, unique_rep_changes[0].time)


def update_primary(change_uuids):
    # finds the ChangeLogs unique to the replica, using UUIDs
    rep_changes = ChangeLog.objects(uuid__nin=change_uuids)
    if len(rep_changes) == 0:
        return
    rep_changes = rep_changes.order_by('+time')
    for change_log in rep_changes:
        apply_change(change_log, db_alias=PRIMARY_DB_ALIAS)


def apply_change(change_log, db_alias='default'):
    change = change_log.change
    if isinstance(change, Addition):
        apply_addition(change, db_alias=db_alias)
    if isinstance(change, Deletion):
        apply_deletion(change, db_alias=db_alias)
    if isinstance(change, Update):
        apply_update(change, db_alias=db_alias)
    change_log.switch_db(db_alias)
    change_log.save()


def apply_addition(change, db_alias='default'):
    Document = eval(change.collection)
    doc = Document(**change.doc_added)
    doc.switch_db(db_alias)
    doc.save()


def apply_deletion(change, db_alias='default'):
    Document = eval(change.collection)
    with switch_db(Document, db_alias) as Doc:
        Doc.objects.get(uuid=change.doc_uuid).delete()


def apply_update(change, db_alias='default'):
    Document = eval(change.collection)
    with switch_db(Document, db_alias) as Doc:
        d = Doc.objects.get(uuid=change.doc_uuid)
    d.switch_db(db_alias)
    d.update(**change.fields_changed)
    d.save()


def searchable_dict(object_dict):
    # print("Making search dict from " + str(object_dict))
    to_return = {}
    for key in object_dict:
        if key[0] == '_':
            pass
        elif isinstance(object_dict[key], ObjectId):
            pass
        else:
            to_return.update({key: object_dict[key]})
    # print("Trimmed to " + str(to_return))
    return to_return


def buildable_dict(object_dict):
    # print("Making build dict from " + str(object_dict))
    to_return = {}
    for key in object_dict:
        if key[0] == '_':
            pass
        else:
            to_return.update({key: object_dict[key]})
    # print("Trimmed to " + str(to_return))
    return to_return

