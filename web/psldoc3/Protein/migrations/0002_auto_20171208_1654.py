# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-08 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Protein', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='testfile',
            field=models.FileField(default=1, max_length=50000, upload_to=b''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='comment',
            field=models.FileField(max_length=50000, upload_to=b''),
        ),
    ]