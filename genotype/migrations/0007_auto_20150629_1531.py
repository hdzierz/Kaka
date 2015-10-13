# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('genotype', '0006_auto_20150626_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='marker',
            name='dtt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='marker',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='primer',
            name='dtt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='primer',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='primerob',
            name='dtt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='primerob',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='primertype',
            name='dtt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='primertype',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
    ]
