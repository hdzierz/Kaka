# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seafood', '0003_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='fish',
            name='tow',
            field=models.ForeignKey(default=1, to='seafood.Tow'),
            preserve_default=False,
        ),
    ]
