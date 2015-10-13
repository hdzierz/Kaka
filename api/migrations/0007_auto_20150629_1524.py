# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import jsonfield.fields
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20150626_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='biosubject',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 15, 23, 20, 84438), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='biosubject',
            name='geo',
            field=jsonfield.fields.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='diet',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 15, 23, 34, 804426), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='diet',
            name='geo',
            field=jsonfield.fields.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='instrument',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 23, 46, 589023, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instrument',
            name='geo',
            field=jsonfield.fields.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='protein',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 23, 53, 959835, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='protein',
            name='geo',
            field=jsonfield.fields.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='samplemethod',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 23, 56, 76283, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='samplemethod',
            name='geo',
            field=jsonfield.fields.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='species',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 23, 57, 871351, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='species',
            name='geo',
            field=jsonfield.fields.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='study',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 23, 59, 854069, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='study',
            name='geo',
            field=jsonfield.fields.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='studyarea',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 24, 1, 797152, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studyarea',
            name='geo',
            field=jsonfield.fields.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='studygroup',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 24, 3, 680283, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studygroup',
            name='geo',
            field=jsonfield.fields.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='tissue',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 24, 5, 620974, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tissue',
            name='geo',
            field=jsonfield.fields.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='treatment',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 24, 12, 745835, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='treatment',
            name='geo',
            field=jsonfield.fields.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='unit',
            name='dtt',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 29, 3, 24, 15, 816555, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unit',
            name='geo',
            field=jsonfield.fields.JSONField(default=None),
        ),
    ]
