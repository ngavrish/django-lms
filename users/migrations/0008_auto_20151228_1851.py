# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-28 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20151228_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=30, unique=True),
        ),
    ]
