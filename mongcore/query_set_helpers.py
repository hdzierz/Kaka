from mongoengine.context_managers import switch_db
from .models import Experiment, DataSource, Feature
from kaka.settings import TEST_DB_ALIAS


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


def build_dict(document, testing=False):
    object_dict = document.to_mongo().to_dict()
    to_return = {}
    if isinstance(document, Feature):
        ref_fields = get_ref_fields(document, testing)
    for key in object_dict:
        if key[0] == '_':
            pass
        elif key is "study" or key is "datasource":
            to_return.update({key: ref_fields[key].name})
        else:
            to_return.update({key: object_dict[key]})
    # print("Trimmed to " + str(to_return))
    return to_return


def query_to_csv_rows_list(query, testing=False):
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
    # Header row from Genotype document fields
    header = []
    head_dict = query_set[0].to_mongo().to_dict()
    keys = head_dict.keys()
    for doc in query_set[1:]:
        doc_keys = doc.to_mongo().to_dict().keys()
        for key in doc_keys:
            if key not in keys:
                keys.append[key]
    sorted_keys = sorted(keys)
    for key in sorted_keys:
        if key[0] != '_':
            if key is "study" or key is "datasource":
                header.append(key + "__name")
            else:
                header.append(key)
    header_row = ','.join(header)
    return header_row, sorted_keys
