# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_datasource_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasource',
            name='values',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]
