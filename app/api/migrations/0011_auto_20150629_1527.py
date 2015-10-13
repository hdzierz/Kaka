# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20150629_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='biosubject',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 27, 35, 771989, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='diet',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 27, 35, 771989, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='instrument',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 27, 35, 771989, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='protein',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 27, 35, 771989, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='samplemethod',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 27, 35, 771989, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='species',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 27, 35, 771989, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='study',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 27, 35, 771989, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='studyarea',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 27, 35, 771989, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='studygroup',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 27, 35, 771989, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='tissue',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 27, 35, 771989, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='treatment',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 27, 35, 771989, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='unit',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 27, 35, 771989, tzinfo=utc)),
        ),
    ]
