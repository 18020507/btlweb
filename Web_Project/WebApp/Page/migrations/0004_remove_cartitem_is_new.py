# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-12-04 03:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Page', '0003_auto_20201203_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='is_new',
        ),
    ]
