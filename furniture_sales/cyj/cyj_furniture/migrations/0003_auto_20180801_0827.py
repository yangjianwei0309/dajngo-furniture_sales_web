# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-01 08:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cyj_furniture', '0002_auto_20180801_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='furniture',
            name='img',
            field=models.CharField(max_length=100, null=True, verbose_name='图片名'),
        ),
    ]
