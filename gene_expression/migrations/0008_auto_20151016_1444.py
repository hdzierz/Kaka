# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gene_expression', '0007_auto_20150629_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gene',
            name='datasource',
        ),
        migrations.RemoveField(
            model_name='target',
            name='datasource',
        ),
    ]
