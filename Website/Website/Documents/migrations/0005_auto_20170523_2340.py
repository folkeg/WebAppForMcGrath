# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-23 23:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0004_auto_20170523_2338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.CharField(max_length=500)),
            ],
        ),
        migrations.RenameField(
            model_name='ocrcoordinates',
            old_name='document_Date_MarkingType',
            new_name='document_date_MarkingType',
        ),
        migrations.RenameField(
            model_name='ocrcoordinates',
            old_name='document_Date_Regex',
            new_name='document_date_Regex',
        ),
        migrations.RenameField(
            model_name='ocrcoordinates',
            old_name='document_Date_bottom',
            new_name='document_date_bottom',
        ),
        migrations.RenameField(
            model_name='ocrcoordinates',
            old_name='document_Date_left',
            new_name='document_date_left',
        ),
        migrations.RenameField(
            model_name='ocrcoordinates',
            old_name='document_Date_letterset',
            new_name='document_date_letterset',
        ),
        migrations.RenameField(
            model_name='ocrcoordinates',
            old_name='document_Date_right',
            new_name='document_date_right',
        ),
        migrations.RenameField(
            model_name='ocrcoordinates',
            old_name='document_Date_top',
            new_name='document_date_top',
        ),
        migrations.RenameField(
            model_name='ocrcoordinates',
            old_name='locument_Date_texttype',
            new_name='locument_date_texttype',
        ),
    ]