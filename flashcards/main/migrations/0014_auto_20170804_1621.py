# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_decks_languages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='desc',
            field=models.CharField(default='', max_length=256, verbose_name='Opis'),
        ),
    ]
