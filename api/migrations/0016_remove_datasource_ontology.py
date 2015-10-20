# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20151016_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datasource',
            name='ontology',
        ),
    ]
