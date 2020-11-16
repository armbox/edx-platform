# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2020-11-16 08:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0004_delete_historical_credit_records'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='creditrequirementstatus',
            options={'verbose_name_plural': ' \ud06c\ub808\ub527 \uc694\uac74 \uc0c1\ud0dc '},
        ),
        migrations.AlterField(
            model_name='creditconfig',
            name='cache_ttl',
            field=models.PositiveIntegerField(default=0, help_text=' \ucd08 \ub2e8\uc704\ub85c \uc9c0\uc815\ub429\ub2c8\ub2e4. \uc774\uac83\uc744 0\ubcf4\ub2e4 \ud070 \uac12\uc73c\ub85c \uc124\uc815\ud558\uc5ec \uce90\uc2f1\uc744 \ud65c\uc131\ud654\ud558\uc2ed\uc2dc\uc624.', verbose_name='\uce90\uc2dc\uac00 \uc720\uc9c0\ub418\ub294 \uc2dc\uac04'),
        ),
    ]
