# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_datasource_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biosubject',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='values',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='diet',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='protein',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='samplemethod',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='species',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='study',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='studyarea',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='studygroup',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='term',
            name='values',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='tissue',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='unit',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
    ]
