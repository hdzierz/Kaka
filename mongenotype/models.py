import mongoengine
from django.db import models
from mongcore.models import Feature
from core.models import Feature as OldFeature

from django.core.urlresolvers import reverse

class Chromosome(Feature):
    no = mongoengine.StringField(max_length=10)

    def __unicode__(self):
        return self.GetName()

    def GetName(self):
        return self.no


class Genotype(Feature):
    ebrida_id = mongoengine.StringField(max_length=255)
    kea_id = mongoengine.StringField(max_length=255)

    def __unicode__(self):
        return self.GetName()

    def GetName(self):
        return self.kea_id + '/' + self.ebrida_id


class Marker(Feature):
    ebrida_id = mongoengine.StringField(max_length=255)
    kea_id = mongoengine.StringField(max_length=255)
    sex = mongoengine.StringField(max_length=5)

    def __unicode__(self):
        return self.GetName()
    
    def GetName(self):
        return self.kea_id + '/' + self.ebrida_id

    def get_absolute_url(self):
        return reverse('marker-detail', kwargs={'pk': self.pk})


class OldMarker(OldFeature):
    ebrida_id = mongoengine.StringField(max_length=255)
    kea_id = mongoengine.StringField(max_length=255)
    sex = mongoengine.StringField(max_length=5)

    def __unicode__(self):
        return self.GetName()

    def GetName(self):
        return self.kea_id + '/' + self.ebrida_id

    def get_absolute_url(self):
        return reverse('marker-detail', kwargs={'pk': self.pk})


class Primer(Feature):
    def __unicode__(self):
        return self.name

    def GetName(self):
        return self.name


class PrimerType(Feature):
    def __unicode__(self):
        return self.name

    def GetName(self):
        return self.name


class OldPrimer(OldFeature):
    def __unicode__(self):
        return self.name

    def GetName(self):
        return self.name


class OldPrimerType(OldFeature):
    def __unicode__(self):
        return self.name

    def GetName(self):
        return self.name


class PrimerOb(Feature):
    primer = mongoengine.ReferenceField(Primer)
    primer_type = mongoengine.ReferenceField(PrimerType)
    def __unicode__(self):
        return self.name

    def GetName(self):
        return self.name


class OldPrimerOb(OldFeature):
    primer = models.ForeignKey(OldPrimer)
    primer_type = models.ForeignKey(OldPrimerType)
    def __unicode__(self):
        return self.name

    def GetName(self):
        return self.name

#primerob
#    genotype | primertype
#    genotype | markerob
#    genotype | primer
#    genotype | primertail


# Create your models here.
