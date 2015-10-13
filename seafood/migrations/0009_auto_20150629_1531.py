# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('seafood', '0008_auto_20150626_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='dtt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='city',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='crew',
            name='dtt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='crew',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='fish',
            name='dtt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='fish',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='staff',
            name='dtt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='staff',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='tow',
            name='dtt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='tow',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='tree',
            name='dtt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='tree',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='trip',
            name='dtt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='trip',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='vessel',
            name='dtt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='vessel',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
    ]
