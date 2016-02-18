from mongoengine.context_managers import switch_db
from .models import Experiment, DataSource, Feature
from kaka.settings import TEST_DB_ALIAS


def fetch_or_save(Document, db_alias='default', search_dict=None, **kwargs):
    """
    Searches through the collection of the given document class for a document
    who's field values match the values in the search_dict (or the kwargs if
    no search_dict was given).
    If one is found, returns the found document along with a boolean False to
    indicate that no new documents were created
    If one is not found, creates and saves a new document of the given document
    class from the kwargs. Returns the new document with a boolean True to
    indicate that a new document was created

    :param Document: Class of document to fetch or save
    :param db_alias: Alias of database to search through
    :param search_dict: Dictionary of values to query document collection with
    :param kwargs: Values to create document with if no document found. Also
                   values to query document collection with if search_dict=None
    :return: Document found or created and boolean that is True if document created
    """
    if search_dict is None:
        search_dict = kwargs
    if 'id' in kwargs:
        search_dict = {'id': search_dict['id']}
    try:
        doc = Document.objects.get(**search_dict)
    except Document.DoesNotExist:
        doc = Document(**kwargs)
        doc.switch_db(db_alias)
        doc.save()
        return doc, True
    else:
        return doc, False


def build_dict(document, testing=False):
    """
    Returns a dictionary built from a document's fields. Does not include keys
    which start with '_' as they are metadata fields. For document values in
    reference fields just uses the value's name
    :param document: Document to build dictionary from
    :param testing: If method called in unit test (to determine which db to get
                    reference values from)
    :return: Dictionary representation of document
    """
    object_dict = document.to_mongo().to_dict()
    to_return = {}
    if isinstance(document, Feature):
        ref_fields = get_ref_fields(document, testing)
    for key in object_dict:
        if key[0] == '_':
            pass
        elif key is "study" or key is "datasource":
            to_return.update({key + "__name": ref_fields[key].name})
        else:
            to_return.update({key: object_dict[key]})
    return to_return


def query_to_csv_rows_list(query, testing=False):
    """
    Builds a list of string representations of rows of a csv file that represents
    the given query set
    :param query: Query set to build list from
    :param testing: If method called in unit test (to determine which db to get
                    reference values from)
    :return: List of string rows of csv file representing query
    """
    header_row, sorted_keys = write_header_row(query)
    rows = [header_row]
    rows.extend(rows_from_query(query, sorted_keys, testing=testing))
    return rows


def rows_from_query(query, sorted_keys, testing=False):
    rows = []
    # csv row for each document
    for gen in query:
        if isinstance(gen, Feature):
            ref_fields = get_ref_fields(gen, testing)

        gen_dic = gen.to_mongo().to_dict()
        row = []

        for key in sorted_keys:
            if key[0] != '_':
                if key not in gen_dic.keys():
                    row.append("")
                elif key is "study" or key is "datasource":
                    row.append(ref_fields[key].name)
                elif key is 'obs' or isinstance(gen_dic[key], dict):
                    row.append('"' + print_ordered_dict(gen_dic[key]) + '"')
                else:
                    row.append(str(gen_dic[key]).strip())

        row_string = ','.join(row)
        rows.append(row_string)

    return rows


def get_ref_fields(gen, testing):
    ref_fields = {"study": gen.study, "datasource": gen.datasource}
    if testing:
        # Reference fields would only hold database references instead of the actual
        # document, so need to query the test database for the documents
        study_son = ref_fields['study'].as_doc()
        ds_son = ref_fields['datasource'].as_doc()
        study_id = study_son.get('$id')
        with switch_db(Experiment, TEST_DB_ALIAS) as Exper:
            ref_fields['study'] = Exper.objects.get(id=study_id)
        ds_id = ds_son.get('$id')
        with switch_db(DataSource, TEST_DB_ALIAS) as Dat:
            ref_fields['datasource'] = Dat.objects.get(id=ds_id)
    return ref_fields


def print_ordered_dict(dictionary):
    sorted_keys = sorted(dictionary.keys())
    strings = []
    for key in sorted_keys:
        dict_entry_str = "'" + key + "':'" + dictionary[key] + "'"
        strings.append(dict_entry_str)
    return "{" + ','.join(strings) + "}"


def write_header_row(query_set):
    # builds top row of csv file with names of all the fields
    header = []
    # Gets name of all the fields of the first document in the queryset
    head_dict = query_set[0].to_mongo().to_dict()
    dict_keys = head_dict.keys()
    keys = []
    for key in dict_keys:
        keys.append(key)
    # Checks the other documents in the queryset for fields the first document
    # did not have
    for doc in query_set[1:]:
        doc_keys = doc.to_mongo().to_dict().keys()
        for key in doc_keys:
            if key not in keys:
                keys.append(key)

    # Builds a string of the sorted keys without metadata keys and '__name' appended
    # to keys for reference fields
    sorted_keys = sorted(keys)
    for key in sorted_keys:
        if key[0] != '_':
            if key is "study" or key is "datasource":
                header.append(key + "__name")
            else:
                header.append(key)
    header_row = ','.join(header)
    return header_row, sorted_keys
