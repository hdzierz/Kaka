# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seafood', '0009_auto_20150629_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='crew',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='fish',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='tow',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='tree',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='vessel',
            name='datasource',
        ),
    ]
