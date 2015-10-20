# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20151016_1448'),
        ('seafood', '0010_auto_20151016_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='crew',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='fish',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='staff',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='tow',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='tree',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='trip',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='vessel',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
    ]
