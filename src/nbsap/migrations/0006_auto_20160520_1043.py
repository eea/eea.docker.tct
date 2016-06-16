# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-20 15:43
from __future__ import unicode_literals

from django.db import migrations


def _migrate_eu_target_fowards(apps, schema_editor):
    EuAichiStrategy = apps.get_model('nbsap', 'EuAichiStrategy')
    for strategy in EuAichiStrategy.objects.all():
        strategy.eu_targets.add(strategy.eu_target)


def _migrate_eu_target_backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('nbsap', '0005_auto_20160519_0949'),
    ]

    operations = [
        migrations.RunPython(_migrate_eu_target_fowards,
                             _migrate_eu_target_backwards)
    ]