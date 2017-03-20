# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-19 22:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.CharField(blank=True, choices=[(None, b'-----'), (b'Valid', b'Valid'), (b'Sold', b'Sold')], max_length=500),
        ),
        migrations.AlterField(
            model_name='document',
            name='document_date',
            field=models.DateField(),
        ),
    ]