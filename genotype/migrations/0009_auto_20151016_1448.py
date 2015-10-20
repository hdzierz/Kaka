# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20151016_1448'),
        ('genotype', '0008_auto_20151016_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='marker',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='primer',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='primerob',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='primertype',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
    ]
