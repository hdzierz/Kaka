import mongoengine
from uuid import uuid4
from .query_set_helpers import build_dict
from datetime import datetime

logging = True


class Change(mongoengine.EmbeddedDocument):
    collection = mongoengine.StringField()
    doc_uuid = mongoengine.UUIDField()

    meta = {
        'allow_inheritance': True, 'abstract': True
    }


class ChangeLog(mongoengine.Document):
    time = mongoengine.DateTimeField(default=datetime.now())
    uuid = mongoengine.UUIDField(unique=True)
    change = mongoengine.EmbeddedDocumentField(Change)


class Addition(Change):
    doc_added = mongoengine.DictField()


class Deletion(Change):
    pass


class Update(Change):
    fields_changed = mongoengine.DictField()


def log_addition(document):

    if logging:
        change = ChangeLog(
            uuid=uuid4(), change=Addition(
                doc_uuid=document.uuid, collection=document.__class__.__name__,
                doc_added=build_dict(document)
            )
        )
        change.save()


def log_deletion(document):

    if logging:
        change = ChangeLog(
            uuid=uuid4(), change=Deletion(
                doc_uuid=document.uuid, collection=document.__class__.__name__
            )
        )
        change.save()


def log_update(document, change_dict):

    if logging:
        change = ChangeLog(
            uuid=uuid4(), change=Update(
                doc_uuid=document.uuid, collection=document.__class__.__name__,
                fields_changed=change_dict
            )
        )
        change.save()
