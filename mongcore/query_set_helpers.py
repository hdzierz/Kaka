import uuid


def fetch_or_save(Document, db_alias='default', search_dict=None, **kwargs):
    if search_dict is None:
        search_dict = kwargs
    if 'uuid' in kwargs:
        # print("Searching with uuid!")
        search_dict = {'uuid': search_dict['uuid']}
    # else:
    #     print("No uuid. Searching without ")
    try:
        doc = Document.objects.get(**search_dict)
        # print("Found {0} {1}".format(doc.name, doc.uuid))
    except Document.DoesNotExist:
        # print("Saving {0} in {1}".format(kwargs['name'], db_alias))
        doc = Document(**kwargs)
        if 'uuid' not in kwargs:
            doc.uuid = uuid.uuid4()
        doc.switch_db(db_alias)
        doc.save()
        return doc, True
    except Exception as e:
        print("What is this expception?: " + str(e.__class__))
        raise e
    else:
        return doc, False


def build_dict(document):
    object_dict = document.to_mongo().to_dict()
    to_return = {}
    for key in object_dict:
        if key[0] == '_':
            pass
        else:
            to_return.update({key: object_dict[key]})
    # print("Trimmed to " + str(to_return))
    return to_return
