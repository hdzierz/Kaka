# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gene_expression', '0004_gene_target'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gene',
            name='target',
        ),
    ]
