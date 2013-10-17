# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Link'
        db.create_table(u'nbsap_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'nbsap', ['Link'])

        # Adding model 'Scale'
        db.create_table(u'nbsap_scale', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'nbsap', ['Scale'])

        # Adding model 'AichiIndicator'
        db.create_table(u'nbsap_aichiindicator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('head_indicator', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sub_indicator', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sensitivity', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('validity', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('ease_of_communication', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('sources', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('requirements', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('measurer', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('conventions', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'nbsap', ['AichiIndicator'])

        # Adding M2M table for field scales on 'AichiIndicator'
        m2m_table_name = db.shorten_name(u'nbsap_aichiindicator_scales')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aichiindicator', models.ForeignKey(orm[u'nbsap.aichiindicator'], null=False)),
            ('scale', models.ForeignKey(orm[u'nbsap.scale'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aichiindicator_id', 'scale_id'])

        # Adding M2M table for field links on 'AichiIndicator'
        m2m_table_name = db.shorten_name(u'nbsap_aichiindicator_links')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aichiindicator', models.ForeignKey(orm[u'nbsap.aichiindicator'], null=False)),
            ('link', models.ForeignKey(orm[u'nbsap.link'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aichiindicator_id', 'link_id'])

        # Adding model 'AichiTarget'
        db.create_table(u'nbsap_aichitarget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('description_en', self.gf('django.db.models.fields.TextField')()),
            ('description_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_nl', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'nbsap', ['AichiTarget'])

        # Adding M2M table for field indicators on 'AichiTarget'
        m2m_table_name = db.shorten_name(u'nbsap_aichitarget_indicators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aichitarget', models.ForeignKey(orm[u'nbsap.aichitarget'], null=False)),
            ('aichiindicator', models.ForeignKey(orm[u'nbsap.aichiindicator'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aichitarget_id', 'aichiindicator_id'])

        # Adding M2M table for field other_indicators on 'AichiTarget'
        m2m_table_name = db.shorten_name(u'nbsap_aichitarget_other_indicators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aichitarget', models.ForeignKey(orm[u'nbsap.aichitarget'], null=False)),
            ('aichiindicator', models.ForeignKey(orm[u'nbsap.aichiindicator'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aichitarget_id', 'aichiindicator_id'])

        # Adding model 'AichiGoal'
        db.create_table(u'nbsap_aichigoal', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=1, primary_key=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('title_fr', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('title_nl', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('description_en', self.gf('django.db.models.fields.TextField')()),
            ('description_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_nl', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'nbsap', ['AichiGoal'])

        # Adding M2M table for field targets on 'AichiGoal'
        m2m_table_name = db.shorten_name(u'nbsap_aichigoal_targets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aichigoal', models.ForeignKey(orm[u'nbsap.aichigoal'], null=False)),
            ('aichitarget', models.ForeignKey(orm[u'nbsap.aichitarget'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aichigoal_id', 'aichitarget_id'])

        # Adding model 'NationalAction'
        db.create_table(u'nbsap_nationalaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('title_fr', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('title_nl', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('description_en', self.gf('tinymce.models.HTMLField')()),
            ('description_fr', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('description_nl', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'nbsap', ['NationalAction'])

        # Adding model 'NationalObjective'
        db.create_table(u'nbsap_nationalobjective', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('title_fr', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('title_nl', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('description_en', self.gf('tinymce.models.HTMLField')()),
            ('description_fr', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('description_nl', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['nbsap.NationalObjective'])),
        ))
        db.send_create_signal(u'nbsap', ['NationalObjective'])

        # Adding M2M table for field actions on 'NationalObjective'
        m2m_table_name = db.shorten_name(u'nbsap_nationalobjective_actions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nationalobjective', models.ForeignKey(orm[u'nbsap.nationalobjective'], null=False)),
            ('nationalaction', models.ForeignKey(orm[u'nbsap.nationalaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nationalobjective_id', 'nationalaction_id'])

        # Adding model 'EuAction'
        db.create_table(u'nbsap_euaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('description_en', self.gf('django.db.models.fields.TextField')()),
            ('description_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_nl', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['nbsap.EuAction'])),
        ))
        db.send_create_signal(u'nbsap', ['EuAction'])

        # Adding model 'EuIndicator'
        db.create_table(u'nbsap_euindicator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('title_fr', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('title_nl', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('indicator_type', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
        ))
        db.send_create_signal(u'nbsap', ['EuIndicator'])

        # Adding M2M table for field parent on 'EuIndicator'
        m2m_table_name = db.shorten_name(u'nbsap_euindicator_parent')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_euindicator', models.ForeignKey(orm[u'nbsap.euindicator'], null=False)),
            ('to_euindicator', models.ForeignKey(orm[u'nbsap.euindicator'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_euindicator_id', 'to_euindicator_id'])

        # Adding model 'EuTarget'
        db.create_table(u'nbsap_eutarget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('title_fr', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('title_nl', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('description_en', self.gf('django.db.models.fields.TextField')()),
            ('description_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_nl', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'nbsap', ['EuTarget'])

        # Adding M2M table for field actions on 'EuTarget'
        m2m_table_name = db.shorten_name(u'nbsap_eutarget_actions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('eutarget', models.ForeignKey(orm[u'nbsap.eutarget'], null=False)),
            ('euaction', models.ForeignKey(orm[u'nbsap.euaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['eutarget_id', 'euaction_id'])

        # Adding M2M table for field indicators on 'EuTarget'
        m2m_table_name = db.shorten_name(u'nbsap_eutarget_indicators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('eutarget', models.ForeignKey(orm[u'nbsap.eutarget'], null=False)),
            ('euindicator', models.ForeignKey(orm[u'nbsap.euindicator'], null=False))
        ))
        db.create_unique(m2m_table_name, ['eutarget_id', 'euindicator_id'])

        # Adding model 'EuIndicatorToAichiStrategy'
        db.create_table(u'nbsap_euindicatortoaichistrategy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eu_indicator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='eu_indicator_aichi_strategy', to=orm['nbsap.EuIndicator'])),
        ))
        db.send_create_signal(u'nbsap', ['EuIndicatorToAichiStrategy'])

        # Adding M2M table for field aichi_targets on 'EuIndicatorToAichiStrategy'
        m2m_table_name = db.shorten_name(u'nbsap_euindicatortoaichistrategy_aichi_targets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('euindicatortoaichistrategy', models.ForeignKey(orm[u'nbsap.euindicatortoaichistrategy'], null=False)),
            ('aichitarget', models.ForeignKey(orm[u'nbsap.aichitarget'], null=False))
        ))
        db.create_unique(m2m_table_name, ['euindicatortoaichistrategy_id', 'aichitarget_id'])

        # Adding model 'EuAichiStrategy'
        db.create_table(u'nbsap_euaichistrategy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eu_target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='eu_aichi_strategy', to=orm['nbsap.EuTarget'])),
        ))
        db.send_create_signal(u'nbsap', ['EuAichiStrategy'])

        # Adding M2M table for field aichi_targets on 'EuAichiStrategy'
        m2m_table_name = db.shorten_name(u'nbsap_euaichistrategy_aichi_targets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('euaichistrategy', models.ForeignKey(orm[u'nbsap.euaichistrategy'], null=False)),
            ('aichitarget', models.ForeignKey(orm[u'nbsap.aichitarget'], null=False))
        ))
        db.create_unique(m2m_table_name, ['euaichistrategy_id', 'aichitarget_id'])

        # Adding model 'NationalStrategy'
        db.create_table(u'nbsap_nationalstrategy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('objective', self.gf('django.db.models.fields.related.ForeignKey')(related_name='objective_national_strategy', to=orm['nbsap.NationalObjective'])),
            ('relevant_target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relevant_target_national_strategy', to=orm['nbsap.AichiTarget'])),
        ))
        db.send_create_signal(u'nbsap', ['NationalStrategy'])

        # Adding M2M table for field other_targets on 'NationalStrategy'
        m2m_table_name = db.shorten_name(u'nbsap_nationalstrategy_other_targets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nationalstrategy', models.ForeignKey(orm[u'nbsap.nationalstrategy'], null=False)),
            ('aichitarget', models.ForeignKey(orm[u'nbsap.aichitarget'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nationalstrategy_id', 'aichitarget_id'])

        # Adding M2M table for field eu_targets on 'NationalStrategy'
        m2m_table_name = db.shorten_name(u'nbsap_nationalstrategy_eu_targets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nationalstrategy', models.ForeignKey(orm[u'nbsap.nationalstrategy'], null=False)),
            ('eutarget', models.ForeignKey(orm[u'nbsap.eutarget'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nationalstrategy_id', 'eutarget_id'])

        # Adding M2M table for field eu_actions on 'NationalStrategy'
        m2m_table_name = db.shorten_name(u'nbsap_nationalstrategy_eu_actions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nationalstrategy', models.ForeignKey(orm[u'nbsap.nationalstrategy'], null=False)),
            ('euaction', models.ForeignKey(orm[u'nbsap.euaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nationalstrategy_id', 'euaction_id'])


    def backwards(self, orm):
        # Deleting model 'Link'
        db.delete_table(u'nbsap_link')

        # Deleting model 'Scale'
        db.delete_table(u'nbsap_scale')

        # Deleting model 'AichiIndicator'
        db.delete_table(u'nbsap_aichiindicator')

        # Removing M2M table for field scales on 'AichiIndicator'
        db.delete_table(db.shorten_name(u'nbsap_aichiindicator_scales'))

        # Removing M2M table for field links on 'AichiIndicator'
        db.delete_table(db.shorten_name(u'nbsap_aichiindicator_links'))

        # Deleting model 'AichiTarget'
        db.delete_table(u'nbsap_aichitarget')

        # Removing M2M table for field indicators on 'AichiTarget'
        db.delete_table(db.shorten_name(u'nbsap_aichitarget_indicators'))

        # Removing M2M table for field other_indicators on 'AichiTarget'
        db.delete_table(db.shorten_name(u'nbsap_aichitarget_other_indicators'))

        # Deleting model 'AichiGoal'
        db.delete_table(u'nbsap_aichigoal')

        # Removing M2M table for field targets on 'AichiGoal'
        db.delete_table(db.shorten_name(u'nbsap_aichigoal_targets'))

        # Deleting model 'NationalAction'
        db.delete_table(u'nbsap_nationalaction')

        # Deleting model 'NationalObjective'
        db.delete_table(u'nbsap_nationalobjective')

        # Removing M2M table for field actions on 'NationalObjective'
        db.delete_table(db.shorten_name(u'nbsap_nationalobjective_actions'))

        # Deleting model 'EuAction'
        db.delete_table(u'nbsap_euaction')

        # Deleting model 'EuIndicator'
        db.delete_table(u'nbsap_euindicator')

        # Removing M2M table for field parent on 'EuIndicator'
        db.delete_table(db.shorten_name(u'nbsap_euindicator_parent'))

        # Deleting model 'EuTarget'
        db.delete_table(u'nbsap_eutarget')

        # Removing M2M table for field actions on 'EuTarget'
        db.delete_table(db.shorten_name(u'nbsap_eutarget_actions'))

        # Removing M2M table for field indicators on 'EuTarget'
        db.delete_table(db.shorten_name(u'nbsap_eutarget_indicators'))

        # Deleting model 'EuIndicatorToAichiStrategy'
        db.delete_table(u'nbsap_euindicatortoaichistrategy')

        # Removing M2M table for field aichi_targets on 'EuIndicatorToAichiStrategy'
        db.delete_table(db.shorten_name(u'nbsap_euindicatortoaichistrategy_aichi_targets'))

        # Deleting model 'EuAichiStrategy'
        db.delete_table(u'nbsap_euaichistrategy')

        # Removing M2M table for field aichi_targets on 'EuAichiStrategy'
        db.delete_table(db.shorten_name(u'nbsap_euaichistrategy_aichi_targets'))

        # Deleting model 'NationalStrategy'
        db.delete_table(u'nbsap_nationalstrategy')

        # Removing M2M table for field other_targets on 'NationalStrategy'
        db.delete_table(db.shorten_name(u'nbsap_nationalstrategy_other_targets'))

        # Removing M2M table for field eu_targets on 'NationalStrategy'
        db.delete_table(db.shorten_name(u'nbsap_nationalstrategy_eu_targets'))

        # Removing M2M table for field eu_actions on 'NationalStrategy'
        db.delete_table(db.shorten_name(u'nbsap_nationalstrategy_eu_actions'))


    models = {
        u'nbsap.aichigoal': {
            'Meta': {'ordering': "['code']", 'object_name': 'AichiGoal'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '1', 'primary_key': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {}),
            'description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_nl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'targets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'goals'", 'symmetrical': 'False', 'to': u"orm['nbsap.AichiTarget']"}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'nbsap.aichiindicator': {
            'Meta': {'object_name': 'AichiIndicator'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'conventions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ease_of_communication': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'head_indicator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['nbsap.Link']", 'null': 'True', 'blank': 'True'}),
            'measurer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'requirements': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'scales': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['nbsap.Scale']", 'null': 'True', 'blank': 'True'}),
            'sensitivity': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'sources': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sub_indicator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'validity': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'})
        },
        u'nbsap.aichitarget': {
            'Meta': {'ordering': "['code']", 'object_name': 'AichiTarget'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'description_en': ('django.db.models.fields.TextField', [], {}),
            'description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_nl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicators': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'relevant_target'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['nbsap.AichiIndicator']"}),
            'other_indicators': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'other_targets'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['nbsap.AichiIndicator']"})
        },
        u'nbsap.euaction': {
            'Meta': {'object_name': 'EuAction'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'description_en': ('django.db.models.fields.TextField', [], {}),
            'description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_nl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['nbsap.EuAction']"})
        },
        u'nbsap.euaichistrategy': {
            'Meta': {'ordering': "['eu_target']", 'object_name': 'EuAichiStrategy'},
            'aichi_targets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'eu_aichi_strategy'", 'symmetrical': 'False', 'to': u"orm['nbsap.AichiTarget']"}),
            'eu_target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eu_aichi_strategy'", 'to': u"orm['nbsap.EuTarget']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'nbsap.euindicator': {
            'Meta': {'ordering': "['code']", 'object_name': 'EuIndicator'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_type': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'parent_rel_+'", 'null': 'True', 'to': u"orm['nbsap.EuIndicator']"}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'nbsap.euindicatortoaichistrategy': {
            'Meta': {'ordering': "['eu_indicator']", 'object_name': 'EuIndicatorToAichiStrategy'},
            'aichi_targets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'eu_indicator_aichi_strategy'", 'symmetrical': 'False', 'to': u"orm['nbsap.AichiTarget']"}),
            'eu_indicator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eu_indicator_aichi_strategy'", 'to': u"orm['nbsap.EuIndicator']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'nbsap.eutarget': {
            'Meta': {'ordering': "['code']", 'object_name': 'EuTarget'},
            'actions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'target'", 'symmetrical': 'False', 'to': u"orm['nbsap.EuAction']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'description_en': ('django.db.models.fields.TextField', [], {}),
            'description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_nl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicators': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'indicator'", 'symmetrical': 'False', 'to': u"orm['nbsap.EuIndicator']"}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'nbsap.link': {
            'Meta': {'object_name': 'Link'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'nbsap.nationalaction': {
            'Meta': {'object_name': 'NationalAction'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'description_en': ('tinymce.models.HTMLField', [], {}),
            'description_fr': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'description_nl': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'nbsap.nationalobjective': {
            'Meta': {'object_name': 'NationalObjective'},
            'actions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'objective'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['nbsap.NationalAction']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'description_en': ('tinymce.models.HTMLField', [], {}),
            'description_fr': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'description_nl': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['nbsap.NationalObjective']"}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'nbsap.nationalstrategy': {
            'Meta': {'object_name': 'NationalStrategy'},
            'eu_actions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'national_strategy'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['nbsap.EuAction']"}),
            'eu_targets': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'national_strategy'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['nbsap.EuTarget']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'objective': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'objective_national_strategy'", 'to': u"orm['nbsap.NationalObjective']"}),
            'other_targets': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'other_targets_national_strategy'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['nbsap.AichiTarget']"}),
            'relevant_target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relevant_target_national_strategy'", 'to': u"orm['nbsap.AichiTarget']"})
        },
        u'nbsap.scale': {
            'Meta': {'object_name': 'Scale'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['nbsap']