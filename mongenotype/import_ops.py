from mongenotype.models import *
from mongcore.models import *
from mongcore.imports import ImportOpRegistry, ImportOpValidationRegistry

db_alias = 'default'
created_doc_ids = []


def tt(line, imp):
    print("Hello")

def validate(realm, typ):
    def validate_decorator(fun):
        def func_wrapper(line, imp):
            #val = ImportOpValidatorRegistry.get(realm, typ)
            tt(line, imp)
            return fun(line,imp)
    return validate_decorator

class ImportOp:
    ds = None
    study = None
    createddate = None
    description = None
    gen_col = None
    cfg = None

    #@validate("genotype", "design")
    @staticmethod
    def load_design_op(line, imp):
        d = Design()
        d.phenotype = line["phenotype"]
        d.condition = line["condition"]
        d.typ = line["type"]
        d.study = imp.experiment
        d.experiment = imp.experiment.name
        d.save()
        return imp
   
    @staticmethod
    def validate_design_op(line, imp):
        pass 

    @staticmethod
    def load_op(line, imp):
        #try:
        pr = Genotype(
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
        created_doc_ids.append((Genotype, pr.id))

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
        Genotype.objects.filter(experiment=imp.experiment.name).delete()
        Design.objects.filter(experiment=imp.experiment.name).delete()

ImportOpValidationRegistry.register("genotype","design", ImportOp.validate_design_op)
#ImportOpValidationRegistry.register("genotype","data", ImportOp.validate_design_op)
ImportOpRegistry.register("genotype", "design", ImportOp.load_design_op)
ImportOpRegistry.register("genotype", "data", ImportOp.load_op)
ImportOpRegistry.register("genotype", "clean", ImportOp.clean_op)
