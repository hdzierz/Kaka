# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('genotype', '0005_auto_20150618_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marker',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='primer',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='primerob',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='primertype',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
    ]
