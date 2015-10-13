from .models import *
from django.db import connections


class PinfReport:
    def run():
        pass

    class Meta:
        fields=None
        sequence=None
        exclude=None


class FishDataSourceReport(PinfReport):
    def run(self, config=None):
        if config:
            group = config['ds_group']
            return DataSource.objects.filter(supplier=group, is_active=True)
        else:
            return DataSource.objects.filter(is_active=True)

    class Meta(PinfReport.Meta):
#        fields=("name","group","Level 1","Level 2","Level 3","Level 4","Level 5", "Definition")
        exclude=("obs",)


class FishTermReport(PinfReport):
    def run(self, config=None):
        return Term.objects.filter(group='Seafood')

    class Meta(PinfReport.Meta):
        fields=("name","group","Level 1","Level 2","Level 3","Level 4","Level 5", "Definition")


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


class FishReport(PinfReport):
    name = "fish"
    
    def run(self, config=None):
        if config:
            ds_ids = config['ds']
            return Fish.objects.filter(datasource_id__in=ds_ids)
        else:
            qry = """SELECT seafood_fish.name as Fish, 
                            seafood_fish.obs AS obs, 
                            seafood_tow.name AS Tow, 
                            seafood_tow.obs AS obs1,
                            seafood_trip.name AS Trip,
                            seafood_trip.obs AS obs2
                    FROM seafood_fish 
                    LEFT JOIN seafood_tow 
                        ON seafood_tow.obid=tow_id
                    LEFT JOIN seafood_trip
                        ON seafood_tow.trip_id=seafood_trip.obid
                    """

            cursor = connections['default'].cursor()
            cursor.execute(qry)
            res = dictfetchall(cursor)
            return res

