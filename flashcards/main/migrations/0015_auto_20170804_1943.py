# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20170804_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='desc',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='Opis'),
        ),
    ]