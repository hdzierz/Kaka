# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genotype', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='primerob',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='primerob',
            name='ontology',
        ),
        migrations.RemoveField(
            model_name='primertail',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='primertail',
            name='ontology',
        ),
        migrations.DeleteModel(
            name='PrimerOb',
        ),
        migrations.DeleteModel(
            name='PrimerTail',
        ),
    ]
