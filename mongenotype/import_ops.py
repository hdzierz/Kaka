from mongenotype.models import *
from mongcore.models import *

db_alias = 'default'
created_doc_ids = []

class ImportOp:
    ds = None
    study = None
    createddate = None
    description = None
    gen_col = None
    cfg = None

    @staticmethod
    def load_design_op(line, succ):
        d = Design()
        d.phenotype = line["phenotype"]
        d.condition = line["condition"]
        d.typ = line["type"]
        d.study = ImportOp.study
        d.experiment = ImportOp.study.name
        d.save()

    @staticmethod
    def load_op(line, succ):
        #try:
        pr = Genotype(
            name=line[ImportOp.cfg['Genotype Column']],
            study=ImportOp.study,
            experiment=ImportOp.study.name,
            datasource=ImportOp.ds,
            data_source=ImportOp.ds.name,
            createddate=ImportOp.createddate,
            description=ImportOp.description,
        )
        SaveKVs(pr, line)
        pr.switch_db(db_alias)
        pr.save()
        # add to record of docs saved to db by this run through
        created_doc_ids.append((Genotype, pr.id))

        if not ImportOp.study.targets:
            keys = []
            for key in line.keys():
                key = re.sub('[^0-9a-zA-Z_]+', '_', key)
                keys.append(key)

            ImportOp.study.targets = list(keys)
            ImportOp.study.save()
        #except:
        #    Logger.Error("Line did not save")

        return True

    @staticmethod
    def clean_op():
        pass
        #Genotype.objects.filter(data_source=ImportOp.ds).delete()
        #Design.objects.filter(experiment=ImportOp.study).delete()
        #Experiment.objects.filter(name=ImportOp.study.name).delete()


LoadOps = {
    "Design": ImportOp.load_design_op,
    "Data": ImportOp.load_op
}
