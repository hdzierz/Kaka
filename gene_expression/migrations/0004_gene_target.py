# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gene_expression', '0003_auto_20150623_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='gene',
            name='target',
            field=models.ForeignKey(default=1, to='gene_expression.Target'),
            preserve_default=False,
        ),
    ]
