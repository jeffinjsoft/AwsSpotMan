# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-08 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20180408_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='stacks',
            name='eip',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='stacks',
            name='ip',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='stacks',
            name='public_ip',
            field=models.CharField(blank=True, default='no', max_length=20),
        ),
    ]
