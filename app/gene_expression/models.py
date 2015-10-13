from django.db import models

from api.models import *

from jsonfield import JSONField
# Create your models here.


class Target(Feature):
    species = models.ForeignKey(Species, default=1)
    kea_id = models.CharField(max_length=255)
    ebrida_id = models.CharField(max_length=255)
    file_name = models.TextField()
    column = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)   
    lib_type = models.CharField(max_length=255)

    
class Gene(Feature):
    gene_id = models.CharField(max_length=255)
    length = models.IntegerField()
