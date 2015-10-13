# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('seafood', '0007_staff_initials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='crew',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='fish',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='staff',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='tow',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='tow',
            name='values',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='tree',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='vessel',
            name='obs',
            field=jsonfield.fields.JSONField(),
        ),
    ]
