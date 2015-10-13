# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gene_expression', '0005_remove_gene_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gene',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='target',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
    ]
