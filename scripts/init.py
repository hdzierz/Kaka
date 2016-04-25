from mongcore.models import *

def run():
    dd = DataDir()
    dd.path = "/output/kaka"
    dd.name = "global data sump"
    dd.realm = "None"
    dd.save()


