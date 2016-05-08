from mongcore.models import *

def run():
    dd = DataDir()
    dd.path = "/output/kaka"
    dd.name = "global data dump"
    dd.realm = "None"
    dd.save()

    key = Key()
    key.key = binascii.hexlify(os.urandom(24))
    key.name = "Helge"
    key.email = "helge.dzierzon@plantandfood.co.nz"
    key.save()



