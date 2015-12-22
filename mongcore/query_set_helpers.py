def fetch_or_save(Document, db_alias='default', search_dict=None, **kwargs):
    if search_dict is None:
        search_dict = kwargs
    try:
        # print("======================")
        # print("Searching " + db_alias + " with " + str(search_dict))
        doc = Document.objects.get(**search_dict)
        # print("Found " + str(doc))
        # print("======================")
        return doc, False
    except Document.DoesNotExist:
        # print("Search found nothing")
        # print("Adding " + str(kwargs) + "to " + db_alias)
        doc = Document(**kwargs)
        doc.switch_db(db_alias)
        doc.save()
        # print("Saved " + str(doc))
        # print("======================")
        return doc, True
