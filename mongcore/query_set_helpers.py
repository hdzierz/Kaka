def fetch_or_save(Document, db_alias='default', **kwargs):
    try:
        doc = Document.objects.get(**kwargs)
        return doc, False
    except Document.DoesNotExist:
        doc = Document(**kwargs)
        doc.switch_db(db_alias)
        doc.save()
        return doc, True
