# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-08-10 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Banhang', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='TTs',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
