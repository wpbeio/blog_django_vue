# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-24 06:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('beio_auth', '0007_auto_20170924_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beiouser',
            name='date_of_birth',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='邮箱地址'),
        ),
    ]