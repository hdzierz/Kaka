# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import djorm_pgfulltext.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('name', models.CharField(default=b'unknown', max_length=255)),
                ('alias', models.CharField(default=b'unknown', max_length=255)),
                ('description', models.TextField(default=b'')),
                ('obid', models.AutoField(serialize=False, primary_key=True)),
                ('xreflsid', models.CharField(max_length=255)),
                ('createddate', models.DateTimeField(auto_now_add=True)),
                ('createdby', models.CharField(max_length=255)),
                ('lastupdateddate', models.DateTimeField(auto_now=True)),
                ('lastupdatedby', models.CharField(max_length=50)),
                ('obkeywords', models.TextField()),
                ('statuscode', models.IntegerField(default=1)),
                ('search_index', djorm_pgfulltext.fields.VectorField(default=b'', serialize=False, null=True, editable=False, db_index=True)),
                ('obs', jsonfield.fields.JSONField(default=dict)),
                ('ebrida_id', models.CharField(max_length=255)),
                ('kea_id', models.CharField(max_length=255)),
                ('sex', models.CharField(max_length=5)),
                ('datasource', models.ForeignKey(default=1, to='api.DataSource')),
                ('ontology', models.ForeignKey(default=1, to='api.Ontology')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Primer',
            fields=[
                ('name', models.CharField(default=b'unknown', max_length=255)),
                ('alias', models.CharField(default=b'unknown', max_length=255)),
                ('description', models.TextField(default=b'')),
                ('obid', models.AutoField(serialize=False, primary_key=True)),
                ('xreflsid', models.CharField(max_length=255)),
                ('createddate', models.DateTimeField(auto_now_add=True)),
                ('createdby', models.CharField(max_length=255)),
                ('lastupdateddate', models.DateTimeField(auto_now=True)),
                ('lastupdatedby', models.CharField(max_length=50)),
                ('obkeywords', models.TextField()),
                ('statuscode', models.IntegerField(default=1)),
                ('search_index', djorm_pgfulltext.fields.VectorField(default=b'', serialize=False, null=True, editable=False, db_index=True)),
                ('obs', jsonfield.fields.JSONField(default=dict)),
                ('datasource', models.ForeignKey(default=1, to='api.DataSource')),
                ('ontology', models.ForeignKey(default=1, to='api.Ontology')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrimerOb',
            fields=[
                ('name', models.CharField(default=b'unknown', max_length=255)),
                ('alias', models.CharField(default=b'unknown', max_length=255)),
                ('description', models.TextField(default=b'')),
                ('obid', models.AutoField(serialize=False, primary_key=True)),
                ('xreflsid', models.CharField(max_length=255)),
                ('createddate', models.DateTimeField(auto_now_add=True)),
                ('createdby', models.CharField(max_length=255)),
                ('lastupdateddate', models.DateTimeField(auto_now=True)),
                ('lastupdatedby', models.CharField(max_length=50)),
                ('obkeywords', models.TextField()),
                ('statuscode', models.IntegerField(default=1)),
                ('search_index', djorm_pgfulltext.fields.VectorField(default=b'', serialize=False, null=True, editable=False, db_index=True)),
                ('obs', jsonfield.fields.JSONField(default=dict)),
                ('datasource', models.ForeignKey(default=1, to='api.DataSource')),
                ('ontology', models.ForeignKey(default=1, to='api.Ontology')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrimerTail',
            fields=[
                ('name', models.CharField(default=b'unknown', max_length=255)),
                ('alias', models.CharField(default=b'unknown', max_length=255)),
                ('description', models.TextField(default=b'')),
                ('obid', models.AutoField(serialize=False, primary_key=True)),
                ('xreflsid', models.CharField(max_length=255)),
                ('createddate', models.DateTimeField(auto_now_add=True)),
                ('createdby', models.CharField(max_length=255)),
                ('lastupdateddate', models.DateTimeField(auto_now=True)),
                ('lastupdatedby', models.CharField(max_length=50)),
                ('obkeywords', models.TextField()),
                ('statuscode', models.IntegerField(default=1)),
                ('search_index', djorm_pgfulltext.fields.VectorField(default=b'', serialize=False, null=True, editable=False, db_index=True)),
                ('obs', jsonfield.fields.JSONField(default=dict)),
                ('datasource', models.ForeignKey(default=1, to='api.DataSource')),
                ('ontology', models.ForeignKey(default=1, to='api.Ontology')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrimerType',
            fields=[
                ('name', models.CharField(default=b'unknown', max_length=255)),
                ('alias', models.CharField(default=b'unknown', max_length=255)),
                ('description', models.TextField(default=b'')),
                ('obid', models.AutoField(serialize=False, primary_key=True)),
                ('xreflsid', models.CharField(max_length=255)),
                ('createddate', models.DateTimeField(auto_now_add=True)),
                ('createdby', models.CharField(max_length=255)),
                ('lastupdateddate', models.DateTimeField(auto_now=True)),
                ('lastupdatedby', models.CharField(max_length=50)),
                ('obkeywords', models.TextField()),
                ('statuscode', models.IntegerField(default=1)),
                ('search_index', djorm_pgfulltext.fields.VectorField(default=b'', serialize=False, null=True, editable=False, db_index=True)),
                ('obs', jsonfield.fields.JSONField(default=dict)),
                ('datasource', models.ForeignKey(default=1, to='api.DataSource')),
                ('ontology', models.ForeignKey(default=1, to='api.Ontology')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
