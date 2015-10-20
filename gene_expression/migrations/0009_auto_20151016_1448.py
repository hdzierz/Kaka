# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20151016_1448'),
        ('gene_expression', '0008_auto_20151016_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='gene',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
        migrations.AddField(
            model_name='target',
            name='datasource',
            field=models.ForeignKey(default=1, to='api.DataSource'),
        ),
    ]
