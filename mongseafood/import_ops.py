from mongcore.models import *
from mongcore.imports import *
from .models import *
import datetime

def convert_date(dt):
    return time.strptime(dt, "%d.%m.%Y")


def convert_date_time(dt, default=datetime.datetime.now(), fmt="%d %b %Y  %H:%M:%S"):
    #dt = dt.replace('a.m.', 'AM')
    #dt = dt.replace('p.m.', 'PM')
    tz = get_current_timezone()
    if(dt):
        dt = time.strptime(dt, fmt)
        dt = datetime.datetime.fromtimestamp(time.mktime(dt))
        return make_aware(dt, tz)
    else:
        return make_aware(default, tz)


def convert_boolean(val):
    if val == 'Y':
        return True
    else:
        return False


def convert_int(val):
    try:
        return int(val)
    except Exception:
        return None



class ImportSeafoodOp():
    @staticmethod
    def load_tree_op(line, imp):
        term = Term()
        term.name = "/".join([line["Level 1"], line["Level 2"], line["Level 3"], line["Level 4"], line["Level 5"]])
        term.definition = line["Definition"]
        term.group = "Seafood"
        SaveKVs(term, line)
        term.save()
        tree = Tree()
        tree.experiment_obj = imp.experiment
        tree.experiment = imp.experiment.name
        tree.data_source_obj = imp.data_source
        tree.data_source = imp.data_source.name
        tree.name = "/".join([line["Level 1"], line["Level 2"], line["Level 3"], line["Level 4"], line["Level 5"]])
        SaveKVs(tree, line)
        tree.save()

        return imp

    @staticmethod
    def load_fish_data_op(line, imp):
        sp, created = Species.objects.get_or_create(name=line['Species'])

        trip_name = 'Trip_%d' % line['Trip']
        trip, created = Trip.objects.get_or_create(name=trip_name)

        tow_name = 'Tow_%d' % convert_int(line['Tow'])
        tow, created = Tow.objects.get_or_create(name=tow_name, trip=trip)

        fish_name = 'Fish_' + line['Vessel']  + '_' + str(int(line['Trip']))  + '_' + str(int(line['Tow']))  + '_' + str(int(line['Fish Number']))

        fob = Fish()
        fob.name = fish_name
        fob.recordeddate = datetime.datetime.now()
        fob.trip = trip
        fob.tow = tow
        fob.data_source_obj = imp.data_source
        fob.data_source = imp.data_source.name
        fob.experiment_obj = imp.experiment
        fob.experiment = imp.experiment.name
        SaveKVs(fob, line)
        fob.save()

        keys = []
        for key in line.keys():
            key = re.sub('[^0-9a-zA-Z_]+', '_', key)
            keys.append(key)

        imp.experiment.targets = list(keys)
        imp.experiment.save()

        return imp

    @staticmethod
    def load_tow_op(line, imp):
        sp, created = Species.objects.get_or_create(name='Unknown')
        tow_name = "Tow_" + line["Vessel"] + "_" + str(int(line['Trip'])) + "_" + str(int(line["Tow"]))
        ob = Tow()
        ob.name = tow_name
        ob.recordeddate = datetime.datetime.now()
        ob.data_source_obj = imp.data_source
        ob.data_source = imp.data_source.name
        ob.experiment_obj = imp.experiment
        ob.experiment = imp.experiment.name
        SaveKVs(ob, line)
        ob.save()
        return imp
        
    @staticmethod
    def clean_op(imp):
        Tree.objects.filter(data_source=imp.data_source.name).delete()
        Fish.objects.filter(data_source=imp.data_source.name).delete()
        Tow.objects.filter(data_source=imp.data_source.name).delete()


ImportOpRegistry.register("seafood", "tree", ImportSeafoodOp.load_tree_op)
ImportOpRegistry.register("seafood", "tow", ImportSeafoodOp.load_tow_op)
ImportOpRegistry.register("seafood", "fish", ImportSeafoodOp.load_fish_data_op)
ImportOpRegistry.register("seafood", "clean", ImportSeafoodOp.clean_op)
