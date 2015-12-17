from mongcore.models import Experiment, DataSource
from kaka.settings import PRIMARY_DB_ALIAS
from mongoengine.context_managers import switch_db


def synchronise():
    """
    Ensures that the docs in both the primary and local db match.

    Currently just gets all the docs from the primary db and for each
    doc checks for an exact match in the local, then creates a new doc if
    no matches were found. Then does vice-versa

    TODO: handle updates (currently just makes a new one)
    TODO: handle deletions
    TODO: make more efficient?
    :return:
    """
    update_local_replica()
    update_primary()


def update_local_replica():
    update_local_experiments()
    update_local_data_source()


def update_local_experiments():
    with switch_db(Experiment, PRIMARY_DB_ALIAS) as prim:
        from_primary = prim.objects.all()
    for experi in from_primary:
        try:
            Experiment.objects.get(
                name=experi.name, createddate=experi.createddate,
                pi=experi.pi, createdby=experi.createdby,
                description=experi.description
            )
        except Experiment.DoesNotExist:
            ex = Experiment(
                name=experi.name, createddate=experi.createddate,
                pi=experi.pi, createdby=experi.createdby,
                description=experi.description
            )
            ex.save()


def update_local_data_source():
    with switch_db(DataSource, PRIMARY_DB_ALIAS) as prim:
        from_primary = prim.objects.all()
    for ds in from_primary:
        try:
            DataSource.objects.get(
                name=ds.name, source=ds.source, supplieddate=ds.supplieddate,
                typ=ds.typ, supplier=ds.supplier, comment=ds.comment,
                is_active=ds.is_active
            )
        except DataSource.DoesNotExist:
            datas = DataSource(
                name=ds.name, source=ds.source, supplieddate=ds.supplieddate,
                typ=ds.typ, supplier=ds.supplier, comment=ds.comment,
                is_active=ds.is_active
            )
            datas.save()


def update_primary():
    update_primary_experiments()
    update_primary_data_source()


def update_primary_experiments():
    from_replica = Experiment.objects.all()
    for ex in from_replica:
        with switch_db(Experiment, PRIMARY_DB_ALIAS) as prim:
            try:
                prim.objects.get(
                    name=ex.name, createddate=ex.createddate,
                    pi=ex.pi, createdby=ex.createdby,
                    description=ex.description
                )
            except prim.DoesNotExist:
                experi = Experiment(
                    name=ex.name, createddate=ex.createddate,
                    pi=ex.pi, createdby=ex.createdby,
                    description=ex.description
                )
                experi.switch_db(PRIMARY_DB_ALIAS)
                experi.save()


def update_primary_data_source():
    from_replica = DataSource.objects.all()
    for ds in from_replica:
        with switch_db(DataSource, PRIMARY_DB_ALIAS) as prim:
            try:
                prim.objects.get(
                    name=ds.name, source=ds.source, supplieddate=ds.supplieddate,
                    typ=ds.typ, supplier=ds.supplier, comment=ds.comment,
                    is_active=ds.is_active
                )
            except prim.DoesNotExist:
                datas = DataSource(
                    name=ds.name, source=ds.source, supplieddate=ds.supplieddate,
                    typ=ds.typ, supplier=ds.supplier, comment=ds.comment,
                    is_active=ds.is_active
                )
                datas.switch_db(PRIMARY_DB_ALIAS)
                datas.save()
