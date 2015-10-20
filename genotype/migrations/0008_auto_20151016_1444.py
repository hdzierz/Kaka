# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genotype', '0007_auto_20150629_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marker',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='primer',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='primerob',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='primertype',
            name='datasource',
        ),
    ]
