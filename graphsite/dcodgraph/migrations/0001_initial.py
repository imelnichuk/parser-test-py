# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 14:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountriesValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=60)),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Regions',
            fields=[
                ('region_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.AddField(
            model_name='countriesvalues',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcodgraph.Regions'),
        ),
    ]
