# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-24 20:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assetdocument',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='assetdocument',
            name='document',
        ),
        migrations.DeleteModel(
            name='AssetDocument',
        ),
    ]