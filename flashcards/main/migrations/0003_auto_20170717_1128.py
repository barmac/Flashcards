# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 11:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170712_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flashcard',
            name='users',
        ),
        migrations.AddField(
            model_name='flashcard',
            name='repeat',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='flashcard',
            name='answer',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='flashcard',
            name='question',
            field=models.CharField(max_length=128),
        ),
    ]
