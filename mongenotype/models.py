from django_mongoengine import Document, EmbeddedDocument, fields

from django.db import models
from mongcore.models import Feature, Species

from django.core.urlresolvers import reverse


class FastQ(Feature):
    pass

class Helge(Feature):
    pass


class Genotype(Feature):
    pass


class Primer(Feature):
    ordered_fields = ["species", "name","createdby", "data_source", ]

    species_obj = fields.ReferenceField(Species)
    species = fields.StringField(max_length=255, default='species_unkown')


    def __unicode__(self):
        return self.name

    def GetName(self):
        return self.name


class Marker(Feature):
    ebrida_id = fields.StringField(max_length=255)
    kea_id = fields.StringField(max_length=255)
    species_obj = fields.ReferenceField(Species)
    species = fields.StringField(max_length=255, default='species_unkown')
    primer_obj = fields.ReferenceField(Primer)
    primer = fields.StringField(max_length=255, default='pr_unkown') 

    ordered_fields = ["id", "name","createdby", "species", "createddate", "primer", "Primer_sequence"]

    def __unicode__(self):
        return self.GetName()
    
    def GetName(self):
        return self.name



