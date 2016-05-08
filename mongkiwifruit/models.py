import mongoengine
from django.db import models
from mongcore.models import Feature

from django.core.urlresolvers import reverse


class Phenotype(Feature):
    def __unicode__(self):
        return self.GetName()

    def GetName(self):
        return self.name


