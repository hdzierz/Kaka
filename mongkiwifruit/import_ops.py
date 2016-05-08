from mongenotype.models import *
from mongcore.models import *
from mongcore.imports import ImportOpRegistry
from .models import *

db_alias = 'default'
created_doc_ids = []

class ImportOp:

    @staticmethod
    def load_op(line, imp):
        #try:
        pr = Phenotype(
            name=line[imp.id_column],
            experiment_obj=imp.experiment,
            experiment=imp.experiment.name,
            data_source_obj=imp.data_source,
            data_source=imp.data_source.name,
            createddate=imp.experiment.createddate,
            description=imp.experiment.description,
        )
        SaveKVs(pr, line)
        pr.switch_db(db_alias)
        pr.save()
        # add to record of docs saved to db by this run through
        created_doc_ids.append((Phenotype, pr.id))

        if not imp.experiment.targets:
            keys = []
            for key in line.keys():
                key = re.sub('[^0-9a-zA-Z_]+', '_', key)
                keys.append(key)

            imp.experiment.targets = list(keys)
            imp.experiment.save()
        #except:
        #    Logger.Error("Line did not save")
        return imp


    @staticmethod
    def clean_op(imp):
        Phenotype.objects.filter(experiment=imp.experiment.name).delete()

ImportOpRegistry.register("kiwifruit", "data", ImportOp.load_op)
ImportOpRegistry.register("kiwifruit", "clean", ImportOp.clean_op)
