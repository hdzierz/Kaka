# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20151016_1444'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='term',
            name='datasource',
        ),
        migrations.AddField(
            model_name='biosubject',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='diet',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='instrument',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='protein',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='samplemethod',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='species',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='study',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='studyarea',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='studygroup',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='tissue',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='treatment',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='unit',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
    ]
