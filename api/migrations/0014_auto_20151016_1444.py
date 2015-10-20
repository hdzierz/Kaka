# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20150629_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biosubject',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='diet',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='protein',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='samplemethod',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='species',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='study',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='studyarea',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='studygroup',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='treatment',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='unit',
            name='datasource',
        ),
    ]
