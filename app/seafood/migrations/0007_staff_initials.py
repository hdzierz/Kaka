# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seafood', '0006_remove_trip_species'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='initials',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
