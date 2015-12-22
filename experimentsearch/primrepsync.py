from mongcore.models import Experiment, DataSource
from mongenotype.models import Genotype
from kaka.settings import PRIMARY_DB_ALIAS
from mongoengine.context_managers import switch_db
from mongcore.query_set_helpers import fetch_or_save
from bson.objectid import ObjectId

# TODO: handle updates (currently just makes a new one)
# TODO: handle deletions
# TODO: make more efficient?


def synchronise():
    """
    Ensures that the docs in both the primary and local db match.

    Currently just gets all the docs from the primary db and for each
    doc checks for an exact match in the local, then creates a new doc if
    no matches were found. Then does vice-versa

    :return:
    """
    update_local_replica()
    update_primary()


def update_local_replica():
    update_local_experiments()
    update_local_data_source()
    update_local_genotype()


def update_local_experiments():
    with switch_db(Experiment, PRIMARY_DB_ALIAS) as prim:
        from_primary = prim.objects.all()
    for experi in from_primary:
        fetch_or_save(
            Experiment, name=experi.name, createddate=experi.createddate,
            pi=experi.pi, createdby=experi.createdby,
            description=experi.description
        )


def update_local_data_source():
    with switch_db(DataSource, PRIMARY_DB_ALIAS) as prim:
        from_primary = prim.objects.all()
    for ds in from_primary:
        fetch_or_save(
            DataSource, name=ds.name, source=ds.source,
            supplieddate=ds.supplieddate, typ=ds.typ, supplier=ds.supplier,
            comment=ds.comment, is_active=ds.is_active
        )


def update_local_genotype():
    with switch_db(Genotype, PRIMARY_DB_ALIAS) as Prim:
        from_primary = Prim.objects.all()
    for gen in from_primary:
        gen_dict = gen.to_mongo().to_dict()
        search_dict = searchable_dict(gen_dict)
        build_dict = buildable_dict(gen_dict)
        fetch_or_save(Genotype, search_dict=search_dict, **build_dict)


def update_primary():
    update_primary_experiments()
    update_primary_data_source()
    update_primary_genotype()


def update_primary_experiments():
    from_replica = Experiment.objects.all()
    for ex in from_replica:
        with switch_db(Experiment, PRIMARY_DB_ALIAS) as PrimEx:
            fetch_or_save(
                PrimEx, db_alias=PRIMARY_DB_ALIAS, name=ex.name,
                createddate=ex.createddate, pi=ex.pi, createdby=ex.createdby,
                description=ex.description
            )


def update_primary_data_source():
    from_replica = DataSource.objects.all()
    for ds in from_replica:
        with switch_db(DataSource, PRIMARY_DB_ALIAS) as PrimDS:
            fetch_or_save(
                PrimDS, db_alias=PRIMARY_DB_ALIAS, name=ds.name, source=ds.source,
                supplieddate=ds.supplieddate, typ=ds.typ, supplier=ds.supplier,
                comment=ds.comment, is_active=ds.is_active
            )


def update_primary_genotype():
    from_replica = Genotype.objects.all()
    for gen in from_replica:
        gen_dict = gen.to_mongo().to_dict()
        search_dict = searchable_dict(gen_dict)
        build_dict = buildable_dict(gen_dict)
        with switch_db(Genotype, PRIMARY_DB_ALIAS) as PrimGen:
            fetch_or_save(
                PrimGen, db_alias=PRIMARY_DB_ALIAS, search_dict=search_dict,
                **build_dict
            )


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

