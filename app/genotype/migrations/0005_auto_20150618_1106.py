# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genotype', '0004_auto_20150618_1057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='primerob',
            old_name='primer_tye',
            new_name='primer_type',
        ),
    ]
