# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-22 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tct', '0017_auto_20161025_1211'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NbsapPage',
            new_name='TCTPage',
        ),
        migrations.AlterField(
            model_name='cmstarget',
            name='aichi_targets',
            field=models.ManyToManyField(blank=True, related_name='cms_targets', to='tct.AichiTarget'),
        ),
        migrations.AlterField(
            model_name='ramsartarget',
            name='aichi_targets',
            field=models.ManyToManyField(blank=True, related_name='ramsar_targets', to='tct.AichiTarget'),
        ),
    ]