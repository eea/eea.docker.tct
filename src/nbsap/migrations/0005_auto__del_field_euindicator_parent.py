# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'EuIndicator.parent'
        db.delete_column(u'nbsap_euindicator', 'parent_id')

        # Adding M2M table for field parent on 'EuIndicator'
        m2m_table_name = db.shorten_name(u'nbsap_euindicator_parent')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_euindicator', models.ForeignKey(orm[u'nbsap.euindicator'], null=False)),
            ('to_euindicator', models.ForeignKey(orm[u'nbsap.euindicator'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_euindicator_id', 'to_euindicator_id'])


    def backwards(self, orm):
        # Adding field 'EuIndicator.parent'
        db.add_column(u'nbsap_euindicator', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', null=True, to=orm['nbsap.EuIndicator'], blank=True),
                      keep_default=False)

        # Removing M2M table for field parent on 'EuIndicator'
        db.delete_table(db.shorten_name(u'nbsap_euindicator_parent'))


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
            'Meta': {'ordering': "['title_en']", 'object_name': 'EuIndicator'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_type': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'parent_rel_+'", 'null': 'True', 'to': u"orm['nbsap.EuIndicator']"}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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