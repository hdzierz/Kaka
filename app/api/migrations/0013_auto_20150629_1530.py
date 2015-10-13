# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20150629_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biosubject',
            name='geo',
        ),
        migrations.RemoveField(
            model_name='diet',
            name='geo',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='geo',
        ),
        migrations.RemoveField(
            model_name='protein',
            name='geo',
        ),
        migrations.RemoveField(
            model_name='samplemethod',
            name='geo',
        ),
        migrations.RemoveField(
            model_name='species',
            name='geo',
        ),
        migrations.RemoveField(
            model_name='study',
            name='geo',
        ),
        migrations.RemoveField(
            model_name='studyarea',
            name='geo',
        ),
        migrations.RemoveField(
            model_name='studygroup',
            name='geo',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='geo',
        ),
        migrations.RemoveField(
            model_name='treatment',
            name='geo',
        ),
        migrations.RemoveField(
            model_name='unit',
            name='geo',
        ),
        migrations.AddField(
            model_name='biosubject',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='diet',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='instrument',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='protein',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='samplemethod',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='species',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='study',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='studyarea',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='studygroup',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='tissue',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='treatment',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
        migrations.AddField(
            model_name='unit',
            name='geom',
            field=djgeojson.fields.PointField(default={b'type': b'Point', b'coordinates': [0, 0]}),
        ),
    ]
