# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gene_expression', '0006_auto_20150626_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='gene',
            name='dtt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='gene',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='target',
            name='dtt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='target',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
    ]
