

def fetch_or_save(Document, db_alias='default', search_dict=None, **kwargs):
    if search_dict is None:
        search_dict = kwargs
    if 'id' in kwargs:
        # print("Searching with id!")
        search_dict = {'id': search_dict['id']}
    # else:
    #     print("No id. Searching without ")
    try:
        doc = Document.objects.get(**search_dict)
        # print("Found {0} {1}".format(doc.name, doc.id))
    except Document.DoesNotExist:
        # print("Saving {0} in {1}".format(kwargs['name'], db_alias))
        doc = Document(**kwargs)
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
