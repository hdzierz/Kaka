# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genotype', '0003_primerob'),
    ]

    operations = [
        migrations.AddField(
            model_name='primerob',
            name='primer',
            field=models.ForeignKey(default=4109, to='genotype.Primer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='primerob',
            name='primer_tye',
            field=models.ForeignKey(default=3, to='genotype.PrimerType'),
            preserve_default=False,
        ),
    ]
