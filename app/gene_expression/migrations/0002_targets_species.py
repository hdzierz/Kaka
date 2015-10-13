# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_datasource_source'),
        ('gene_expression', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='targets',
            name='species',
            field=models.ForeignKey(default=1, to='api.Species'),
        ),
    ]
