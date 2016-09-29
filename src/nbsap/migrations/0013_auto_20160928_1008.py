# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-28 15:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('nbsap', '0012_auto_20160615_0542'),
    ]

    operations = [
        migrations.AddField(
            model_name='euaction',
            name='level',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='euaction',
            name='lft',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='euaction',
            name='rght',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='euaction',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='aichigoal',
            name='description_de-de',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='aichigoal',
            name='description_en',
            field=tinymce.models.HTMLField(verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='aichigoal',
            name='description_fr',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='aichigoal',
            name='description_nl',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='euaction',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='nbsap.EuAction'),
        ),
        migrations.AlterField(
            model_name='euaction',
            name='title_de-de',
            field=models.TextField(blank=True, null=True, verbose_name=b'Title'),
        ),
        migrations.AlterField(
            model_name='euaction',
            name='title_en',
            field=models.TextField(verbose_name=b'Title'),
        ),
        migrations.AlterField(
            model_name='euaction',
            name='title_fr',
            field=models.TextField(blank=True, null=True, verbose_name=b'Title'),
        ),
        migrations.AlterField(
            model_name='euaction',
            name='title_nl',
            field=models.TextField(blank=True, null=True, verbose_name=b'Title'),
        ),
        migrations.AlterField(
            model_name='nationalaction',
            name='description_de-de',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='nationalaction',
            name='description_en',
            field=tinymce.models.HTMLField(verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='nationalaction',
            name='description_fr',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='nationalaction',
            name='description_nl',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='nationalaction',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nbsap.Region'),
        ),
        migrations.AlterField(
            model_name='nationalaction',
            name='title_en',
            field=models.TextField(blank=True, max_length=512, verbose_name=b'Title'),
        ),
        migrations.AlterField(
            model_name='nationalindicator',
            name='description_de-de',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='nationalindicator',
            name='description_en',
            field=tinymce.models.HTMLField(blank=True, default=1, verbose_name=b'Description'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='nationalindicator',
            name='description_fr',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='nationalindicator',
            name='description_nl',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='nationalobjective',
            name='description_de-de',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='nationalobjective',
            name='description_en',
            field=tinymce.models.HTMLField(verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='nationalobjective',
            name='description_fr',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='nationalobjective',
            name='description_nl',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='nbsappage',
            name='body_de-de',
            field=models.TextField(blank=True, null=True, verbose_name=b'Body'),
        ),
        migrations.AlterField(
            model_name='nbsappage',
            name='body_en',
            field=models.TextField(blank=True, default=1, verbose_name=b'Body'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='nbsappage',
            name='body_fr',
            field=models.TextField(blank=True, null=True, verbose_name=b'Body'),
        ),
        migrations.AlterField(
            model_name='nbsappage',
            name='body_nl',
            field=models.TextField(blank=True, null=True, verbose_name=b'Body'),
        ),
        migrations.AlterField(
            model_name='nbsappage',
            name='title_de-de',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name=b'Title'),
        ),
        migrations.AlterField(
            model_name='nbsappage',
            name='title_en',
            field=models.CharField(max_length=128, verbose_name=b'Title'),
        ),
        migrations.AlterField(
            model_name='nbsappage',
            name='title_fr',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name=b'Title'),
        ),
        migrations.AlterField(
            model_name='nbsappage',
            name='title_nl',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name=b'Title'),
        ),
    ]