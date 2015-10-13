# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_datasource_ontology'),
        ('seafood', '0004_fish_tow'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='species',
            field=models.ForeignKey(default=1, to='api.Species'),
        ),
    ]
