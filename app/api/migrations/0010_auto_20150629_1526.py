# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20150629_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biosubject',
            name='dtt',
        ),
        migrations.RemoveField(
            model_name='diet',
            name='dtt',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='dtt',
        ),
        migrations.RemoveField(
            model_name='protein',
            name='dtt',
        ),
        migrations.RemoveField(
            model_name='samplemethod',
            name='dtt',
        ),
        migrations.RemoveField(
            model_name='species',
            name='dtt',
        ),
        migrations.RemoveField(
            model_name='study',
            name='dtt',
        ),
        migrations.RemoveField(
            model_name='studyarea',
            name='dtt',
        ),
        migrations.RemoveField(
            model_name='studygroup',
            name='dtt',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='dtt',
        ),
        migrations.RemoveField(
            model_name='treatment',
            name='dtt',
        ),
        migrations.RemoveField(
            model_name='unit',
            name='dtt',
        ),
    ]
