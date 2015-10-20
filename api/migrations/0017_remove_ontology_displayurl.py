# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_remove_datasource_ontology'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ontology',
            name='displayurl',
        ),
    ]
