# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seafood', '0005_trip_species'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='species',
        ),
    ]
