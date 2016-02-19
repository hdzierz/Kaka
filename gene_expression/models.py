import mongoengine

from mongcore.models import Feature, Species


from jsonfield import JSONField
# Create your models here.


class Target(Feature):
    species = mongoengine.ReferenceField(Species, default=1)
    kea_id = mongoengine.StringField(max_length=255)
    ebrida_id = mongoengine.StringField(max_length=255)
    file_name = mongoengine.StringField()
    column = mongoengine.StringField(max_length=255)
    condition = mongoengine.StringField(max_length=255)
    lib_type = mongoengine.StringField(max_length=255)

    
class Gene(Feature):
    gene_id = mongoengine.StringField(max_length=255)
    length = mongoengine.IntField()
