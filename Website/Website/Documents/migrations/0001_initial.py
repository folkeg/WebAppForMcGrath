# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-20 23:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalAgency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_agency', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacture_name', models.CharField(blank=True, max_length=500)),
                ('serial_number', models.CharField(blank=True, max_length=500)),
                ('tag_number', models.CharField(blank=True, max_length=500)),
                ('status', models.CharField(blank=True, choices=[(None, b'-----'), (b'Active', b'Active'), (b'Sold', b'Sold')], max_length=500)),
                ('approval_agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Documents.ApprovalAgency')),
            ],
        ),
        migrations.CreateModel(
            name='AssetType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_type', models.CharField(max_length=500)),
                ('approval_agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Documents.ApprovalAgency')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_date', models.DateField()),
                ('renewal_date', models.DateField(blank=True, null=True)),
                ('a_number', models.CharField(blank=True, max_length=500)),
                ('license_decal_number', models.CharField(blank=True, max_length=500)),
                ('model_number', models.CharField(blank=True, max_length=500)),
                ('document_description', models.CharField(blank=True, max_length=500)),
                ('document_file', models.FileField(blank=True, upload_to=b'uploads/%Y/%m/%d/')),
                ('asset', models.ManyToManyField(blank=True, to='Documents.Asset')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(max_length=500)),
                ('document_type_desc', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='document_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Documents.DocumentType'),
        ),
        migrations.AddField(
            model_name='asset',
            name='asset_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Documents.AssetType'),
        ),
    ]
