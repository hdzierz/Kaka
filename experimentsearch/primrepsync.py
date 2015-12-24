from mongcore import document_change_listener
from mongcore.document_change_listener import ChangeLog, Addition, Deletion, Update
from mongcore.models import Experiment, DataSource
from mongenotype.models import Genotype
from kaka.settings import PRIMARY_DB_ALIAS
from mongoengine.context_managers import switch_db
from mongcore.query_set_helpers import fetch_or_save, build_dict
from bson.objectid import ObjectId
from datetime import datetime


def synchronise():
    """
    Ensures that the docs in both the primary and local db match.

    Currently just gets all the docs from the primary db and for each
    doc checks for an exact match in the local, then creates a new doc if
    no matches were found. Then does vice-versa

    :return:
    """
    document_change_listener.logging = False
    rep_changes = ChangeLog.objects.all()
    change_uuids = rep_changes.scalar('uuid')
    with switch_db(ChangeLog, PRIMARY_DB_ALIAS) as Prim:
        prim_change_uuids = Prim.objects.all().scalar('uuid')
        prim_changes = Prim.objects(uuid__nin=change_uuids)
    if len(prim_changes) == 0:
        update_primary()
    else:
        unique_rep_changes = ChangeLog.objects(uuid__nin=prim_change_uuids)
        unique_rep_changes = unique_rep_changes.order_by("+time")
        prim_changes = prim_changes.order_by("+time")
        earliest = min(prim_changes[0].time, unique_rep_changes[0].time)
        all_changes = rep_changes.insert(prim_changes)
        make_changes = all_changes.filter(time__gte=earliest)
        make_changes = make_changes.order_by("+time")
        for change in make_changes:
            apply_change(change)
            apply_change(change, db_alias=PRIMARY_DB_ALIAS)
    document_change_listener.logging = True


def update_primary():
    with switch_db(ChangeLog, PRIMARY_DB_ALIAS) as Prim:
        prim_changes = Prim.objects.all()
    change_uuids = prim_changes.scalar('uuid')
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

