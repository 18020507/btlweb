# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-12-02 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Page', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='sex',
            field=models.CharField(choices=[('Nam', 'Nam'), ('Nữ', 'Nữ'), ('Khác', 'Khác')], default='1', max_length=10),
        ),
    ]