# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_datasource_ontology'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gene',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='gene',
            name='ontology',
        ),
        migrations.DeleteModel(
            name='Gene',
        ),
    ]
