from django.db import models
from api.models import Feature

from django.core.urlresolvers import reverse


class Marker(Feature):
    ebrida_id = models.CharField(max_length=255)
    kea_id = models.CharField(max_length=255)
    sex = models.CharField(max_length=5)

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


class PrimerOb(Feature):
    primer = models.ForeignKey(Primer)
    primer_type = models.ForeignKey(PrimerType)
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
