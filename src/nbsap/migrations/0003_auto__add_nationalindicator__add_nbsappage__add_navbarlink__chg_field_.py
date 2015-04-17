# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NationalIndicator'
        db.create_table(u'nbsap_nationalindicator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('title_en', self.gf('django.db.models.fields.TextField')(max_length=512)),
            ('title_fr', self.gf('django.db.models.fields.TextField')(max_length=512, null=True, blank=True)),
            ('title_nl', self.gf('django.db.models.fields.TextField')(max_length=512, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('indicator_type', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
        ))
        db.send_create_signal(u'nbsap', ['NationalIndicator'])

        # Adding M2M table for field subindicators on 'NationalIndicator'
        m2m_table_name = db.shorten_name(u'nbsap_nationalindicator_subindicators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_nationalindicator', models.ForeignKey(orm[u'nbsap.nationalindicator'], null=False)),
            ('to_nationalindicator', models.ForeignKey(orm[u'nbsap.nationalindicator'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_nationalindicator_id', 'to_nationalindicator_id'])

        # Adding model 'NbsapPage'
        db.create_table(u'nbsap_nbsappage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('title_fr', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('title_nl', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('body_en', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('body_nl', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'nbsap', ['NbsapPage'])

        # Adding model 'NavbarLink'
        db.create_table(u'nbsap_navbarlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'nbsap', ['NavbarLink'])

        # Adding M2M table for field other_aichi_targets on 'EuIndicatorToAichiStrategy'
        m2m_table_name = db.shorten_name(u'nbsap_euindicatortoaichistrategy_other_aichi_targets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('euindicatortoaichistrategy', models.ForeignKey(orm[u'nbsap.euindicatortoaichistrategy'], null=False)),
            ('aichitarget', models.ForeignKey(orm[u'nbsap.aichitarget'], null=False))
        ))
        db.create_unique(m2m_table_name, ['euindicatortoaichistrategy_id', 'aichitarget_id'])

        # Adding M2M table for field other_indicators on 'EuTarget'
        m2m_table_name = db.shorten_name(u'nbsap_eutarget_other_indicators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('eutarget', models.ForeignKey(orm[u'nbsap.eutarget'], null=False)),
            ('euindicator', models.ForeignKey(orm[u'nbsap.euindicator'], null=False))
        ))
        db.create_unique(m2m_table_name, ['eutarget_id', 'euindicator_id'])

        # Adding M2M table for field national_strategy on 'EuTarget'
        m2m_table_name = db.shorten_name(u'nbsap_eutarget_national_strategy')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('eutarget', models.ForeignKey(orm[u'nbsap.eutarget'], null=False)),
            ('nationalstrategy', models.ForeignKey(orm[u'nbsap.nationalstrategy'], null=False))
        ))
        db.create_unique(m2m_table_name, ['eutarget_id', 'nationalstrategy_id'])


        # Changing field 'EuTarget.title_nl'
        db.alter_column(u'nbsap_eutarget', 'title_nl', self.gf('django.db.models.fields.TextField')(max_length=512, null=True))

        # Changing field 'EuTarget.title_en'
        db.alter_column(u'nbsap_eutarget', 'title_en', self.gf('django.db.models.fields.TextField')(max_length=512))

        # Changing field 'EuTarget.title_fr'
        db.alter_column(u'nbsap_eutarget', 'title_fr', self.gf('django.db.models.fields.TextField')(max_length=512, null=True))
        # Adding M2M table for field other_aichi_targets on 'EuAichiStrategy'
        m2m_table_name = db.shorten_name(u'nbsap_euaichistrategy_other_aichi_targets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('euaichistrategy', models.ForeignKey(orm[u'nbsap.euaichistrategy'], null=False)),
            ('aichitarget', models.ForeignKey(orm[u'nbsap.aichitarget'], null=False))
        ))
        db.create_unique(m2m_table_name, ['euaichistrategy_id', 'aichitarget_id'])


        # Changing field 'AichiGoal.title_nl'
        db.alter_column(u'nbsap_aichigoal', 'title_nl', self.gf('django.db.models.fields.TextField')(max_length=512, null=True))

        # Changing field 'AichiGoal.title_en'
        db.alter_column(u'nbsap_aichigoal', 'title_en', self.gf('django.db.models.fields.TextField')(max_length=512))

        # Changing field 'AichiGoal.description_en'
        db.alter_column(u'nbsap_aichigoal', 'description_en', self.gf('tinymce.models.HTMLField')())

        # Changing field 'AichiGoal.description_nl'
        db.alter_column(u'nbsap_aichigoal', 'description_nl', self.gf('tinymce.models.HTMLField')(null=True))

        # Changing field 'AichiGoal.description_fr'
        db.alter_column(u'nbsap_aichigoal', 'description_fr', self.gf('tinymce.models.HTMLField')(null=True))

        # Changing field 'AichiGoal.title_fr'
        db.alter_column(u'nbsap_aichigoal', 'title_fr', self.gf('django.db.models.fields.TextField')(max_length=512, null=True))
        # Removing M2M table for field eu_targets on 'NationalStrategy'
        db.delete_table(db.shorten_name(u'nbsap_nationalstrategy_eu_targets'))

        # Removing M2M table for field eu_actions on 'NationalStrategy'
        db.delete_table(db.shorten_name(u'nbsap_nationalstrategy_eu_actions'))


        # Changing field 'NationalAction.title_nl'
        db.alter_column(u'nbsap_nationalaction', 'title_nl', self.gf('django.db.models.fields.TextField')(max_length=512, null=True))

        # Changing field 'NationalAction.title_en'
        db.alter_column(u'nbsap_nationalaction', 'title_en', self.gf('django.db.models.fields.TextField')(max_length=512))

        # Changing field 'NationalAction.title_fr'
        db.alter_column(u'nbsap_nationalaction', 'title_fr', self.gf('django.db.models.fields.TextField')(max_length=512, null=True))
        # Adding field 'EuAction.title_en'
        db.add_column(u'nbsap_euaction', 'title_en',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'EuAction.title_fr'
        db.add_column(u'nbsap_euaction', 'title_fr',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'EuAction.title_nl'
        db.add_column(u'nbsap_euaction', 'title_nl',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding M2M table for field national_strategy on 'EuAction'
        m2m_table_name = db.shorten_name(u'nbsap_euaction_national_strategy')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('euaction', models.ForeignKey(orm[u'nbsap.euaction'], null=False)),
            ('nationalstrategy', models.ForeignKey(orm[u'nbsap.nationalstrategy'], null=False))
        ))
        db.create_unique(m2m_table_name, ['euaction_id', 'nationalstrategy_id'])


        # Changing field 'EuIndicator.title_nl'
        db.alter_column(u'nbsap_euindicator', 'title_nl', self.gf('django.db.models.fields.TextField')(max_length=512, null=True))

        # Changing field 'EuIndicator.title_en'
        db.alter_column(u'nbsap_euindicator', 'title_en', self.gf('django.db.models.fields.TextField')(max_length=512))

        # Changing field 'EuIndicator.title_fr'
        db.alter_column(u'nbsap_euindicator', 'title_fr', self.gf('django.db.models.fields.TextField')(max_length=512, null=True))
        # Adding M2M table for field nat_indicators on 'NationalObjective'
        m2m_table_name = db.shorten_name(u'nbsap_nationalobjective_nat_indicators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nationalobjective', models.ForeignKey(orm[u'nbsap.nationalobjective'], null=False)),
            ('nationalindicator', models.ForeignKey(orm[u'nbsap.nationalindicator'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nationalobjective_id', 'nationalindicator_id'])

        # Adding M2M table for field other_nat_indicators on 'NationalObjective'
        m2m_table_name = db.shorten_name(u'nbsap_nationalobjective_other_nat_indicators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nationalobjective', models.ForeignKey(orm[u'nbsap.nationalobjective'], null=False)),
            ('nationalindicator', models.ForeignKey(orm[u'nbsap.nationalindicator'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nationalobjective_id', 'nationalindicator_id'])


        # Changing field 'NationalObjective.title_nl'
        db.alter_column(u'nbsap_nationalobjective', 'title_nl', self.gf('django.db.models.fields.TextField')(max_length=512, null=True))

        # Changing field 'NationalObjective.title_en'
        db.alter_column(u'nbsap_nationalobjective', 'title_en', self.gf('django.db.models.fields.TextField')(max_length=512))

        # Changing field 'NationalObjective.title_fr'
        db.alter_column(u'nbsap_nationalobjective', 'title_fr', self.gf('django.db.models.fields.TextField')(max_length=512, null=True))

    def backwards(self, orm):
        # Deleting model 'NationalIndicator'
        db.delete_table(u'nbsap_nationalindicator')

        # Removing M2M table for field subindicators on 'NationalIndicator'
        db.delete_table(db.shorten_name(u'nbsap_nationalindicator_subindicators'))

        # Deleting model 'NbsapPage'
        db.delete_table(u'nbsap_nbsappage')

        # Deleting model 'NavbarLink'
        db.delete_table(u'nbsap_navbarlink')

        # Removing M2M table for field other_aichi_targets on 'EuIndicatorToAichiStrategy'
        db.delete_table(db.shorten_name(u'nbsap_euindicatortoaichistrategy_other_aichi_targets'))

        # Removing M2M table for field other_indicators on 'EuTarget'
        db.delete_table(db.shorten_name(u'nbsap_eutarget_other_indicators'))

        # Removing M2M table for field national_strategy on 'EuTarget'
        db.delete_table(db.shorten_name(u'nbsap_eutarget_national_strategy'))


        # Changing field 'EuTarget.title_nl'
        db.alter_column(u'nbsap_eutarget', 'title_nl', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))

        # Changing field 'EuTarget.title_en'
        db.alter_column(u'nbsap_eutarget', 'title_en', self.gf('django.db.models.fields.CharField')(max_length=512))

        # Changing field 'EuTarget.title_fr'
        db.alter_column(u'nbsap_eutarget', 'title_fr', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))
        # Removing M2M table for field other_aichi_targets on 'EuAichiStrategy'
        db.delete_table(db.shorten_name(u'nbsap_euaichistrategy_other_aichi_targets'))


        # Changing field 'AichiGoal.title_nl'
        db.alter_column(u'nbsap_aichigoal', 'title_nl', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))

        # Changing field 'AichiGoal.title_en'
        db.alter_column(u'nbsap_aichigoal', 'title_en', self.gf('django.db.models.fields.CharField')(max_length=512))

        # Changing field 'AichiGoal.description_en'
        db.alter_column(u'nbsap_aichigoal', 'description_en', self.gf('django.db.models.fields.TextField')())

        # Changing field 'AichiGoal.description_nl'
        db.alter_column(u'nbsap_aichigoal', 'description_nl', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'AichiGoal.description_fr'
        db.alter_column(u'nbsap_aichigoal', 'description_fr', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'AichiGoal.title_fr'
        db.alter_column(u'nbsap_aichigoal', 'title_fr', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))
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


        # Changing field 'NationalAction.title_nl'
        db.alter_column(u'nbsap_nationalaction', 'title_nl', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))

        # Changing field 'NationalAction.title_en'
        db.alter_column(u'nbsap_nationalaction', 'title_en', self.gf('django.db.models.fields.CharField')(max_length=512))

        # Changing field 'NationalAction.title_fr'
        db.alter_column(u'nbsap_nationalaction', 'title_fr', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))
        # Deleting field 'EuAction.title_en'
        db.delete_column(u'nbsap_euaction', 'title_en')

        # Deleting field 'EuAction.title_fr'
        db.delete_column(u'nbsap_euaction', 'title_fr')

        # Deleting field 'EuAction.title_nl'
        db.delete_column(u'nbsap_euaction', 'title_nl')

        # Removing M2M table for field national_strategy on 'EuAction'
        db.delete_table(db.shorten_name(u'nbsap_euaction_national_strategy'))


        # Changing field 'EuIndicator.title_nl'
        db.alter_column(u'nbsap_euindicator', 'title_nl', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))

        # Changing field 'EuIndicator.title_en'
        db.alter_column(u'nbsap_euindicator', 'title_en', self.gf('django.db.models.fields.CharField')(max_length=512))

        # Changing field 'EuIndicator.title_fr'
        db.alter_column(u'nbsap_euindicator', 'title_fr', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))
        # Removing M2M table for field nat_indicators on 'NationalObjective'
        db.delete_table(db.shorten_name(u'nbsap_nationalobjective_nat_indicators'))

        # Removing M2M table for field other_nat_indicators on 'NationalObjective'
        db.delete_table(db.shorten_name(u'nbsap_nationalobjective_other_nat_indicators'))


        # Changing field 'NationalObjective.title_nl'
        db.alter_column(u'nbsap_nationalobjective', 'title_nl', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))

        # Changing field 'NationalObjective.title_en'
        db.alter_column(u'nbsap_nationalobjective', 'title_en', self.gf('django.db.models.fields.CharField')(max_length=512))

        # Changing field 'NationalObjective.title_fr'
        db.alter_column(u'nbsap_nationalobjective', 'title_fr', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))

    models = {
        u'nbsap.aichigoal': {
            'Meta': {'ordering': "['code']", 'object_name': 'AichiGoal'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '1', 'primary_key': 'True'}),
            'description_en': ('tinymce.models.HTMLField', [], {}),
            'description_fr': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'description_nl': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'targets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'goals'", 'symmetrical': 'False', 'to': u"orm['nbsap.AichiTarget']"}),
            'title_en': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'title_fr': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
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
            'national_strategy': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'eu_actions'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['nbsap.NationalStrategy']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['nbsap.EuAction']"}),
            'title_en': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'title_fr': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        u'nbsap.euaichistrategy': {
            'Meta': {'ordering': "['eu_target']", 'object_name': 'EuAichiStrategy'},
            'aichi_targets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'eu_aichi_strategy'", 'symmetrical': 'False', 'to': u"orm['nbsap.AichiTarget']"}),
            'eu_target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eu_aichi_strategy'", 'to': u"orm['nbsap.EuTarget']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other_aichi_targets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'eu_other_aichi_strategy'", 'blank': 'True', 'to': u"orm['nbsap.AichiTarget']"})
        },
        u'nbsap.euindicator': {
            'Meta': {'ordering': "['code']", 'object_name': 'EuIndicator'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_type': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'parents'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['nbsap.EuIndicator']"}),
            'title_en': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'title_fr': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'nbsap.euindicatortoaichistrategy': {
            'Meta': {'ordering': "['eu_indicator']", 'object_name': 'EuIndicatorToAichiStrategy'},
            'aichi_targets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'eu_indicator_aichi_strategy'", 'symmetrical': 'False', 'to': u"orm['nbsap.AichiTarget']"}),
            'eu_indicator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eu_indicator_aichi_strategy'", 'to': u"orm['nbsap.EuIndicator']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other_aichi_targets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'eu_indicator_other_aichi_strategy'", 'blank': 'True', 'to': u"orm['nbsap.AichiTarget']"})
        },
        u'nbsap.eutarget': {
            'Meta': {'ordering': "['code']", 'object_name': 'EuTarget'},
            'actions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'target'", 'blank': 'True', 'to': u"orm['nbsap.EuAction']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'description_en': ('django.db.models.fields.TextField', [], {}),
            'description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_nl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'targets'", 'blank': 'True', 'to': u"orm['nbsap.EuIndicator']"}),
            'national_strategy': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'eu_targets'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['nbsap.NationalStrategy']"}),
            'other_indicators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'other_targets'", 'blank': 'True', 'to': u"orm['nbsap.EuIndicator']"}),
            'title_en': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'title_fr': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
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
            'title_en': ('django.db.models.fields.TextField', [], {'max_length': '512', 'blank': 'True'}),
            'title_fr': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'nbsap.nationalindicator': {
            'Meta': {'ordering': "['code']", 'object_name': 'NationalIndicator'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_type': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'subindicators': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'parents'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['nbsap.NationalIndicator']"}),
            'title_en': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'title_fr': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'nbsap.nationalobjective': {
            'Meta': {'object_name': 'NationalObjective'},
            'actions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'objective'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['nbsap.NationalAction']"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'description_en': ('tinymce.models.HTMLField', [], {}),
            'description_fr': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'description_nl': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nat_indicators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'nat_objectives'", 'blank': 'True', 'to': u"orm['nbsap.NationalIndicator']"}),
            'other_nat_indicators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'other_nat_objectives'", 'blank': 'True', 'to': u"orm['nbsap.NationalIndicator']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['nbsap.NationalObjective']"}),
            'title_en': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'title_fr': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'nbsap.nationalstrategy': {
            'Meta': {'object_name': 'NationalStrategy'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'objective': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'objective_national_strategy'", 'to': u"orm['nbsap.NationalObjective']"}),
            'other_targets': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'other_targets_national_strategy'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['nbsap.AichiTarget']"}),
            'relevant_target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relevant_target_national_strategy'", 'to': u"orm['nbsap.AichiTarget']"})
        },
        u'nbsap.navbarlink': {
            'Meta': {'object_name': 'NavbarLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'nbsap.nbsappage': {
            'Meta': {'object_name': 'NbsapPage'},
            'body_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'body_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body_nl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'nbsap.scale': {
            'Meta': {'object_name': 'Scale'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['nbsap']