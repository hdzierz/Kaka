from django.contrib import admin

# Register your models here.

from .models import *
from genotype.models import *


admin.site.register(DataSource)
admin.site.register(Species)
admin.site.register(Ontology)
admin.site.register(Term)
admin.site.register(Marker)
admin.site.register(Primer)
admin.site.register(PrimerType)
