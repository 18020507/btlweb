# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-12-03 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Page', '0002_auto_20201202_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_new',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='is_new',
            field=models.BooleanField(default=True),
        ),
    ]