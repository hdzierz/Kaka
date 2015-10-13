# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20150623_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasource',
            name='source',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
