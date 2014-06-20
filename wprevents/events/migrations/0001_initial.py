# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FunctionalArea'
        db.create_table(u'events_functionalarea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('color', self.gf('django.db.models.fields.CharField')(default='red-1', max_length=20)),
        ))
        db.send_create_signal(u'events', ['FunctionalArea'])

        # Adding model 'Space'
        db.create_table(u'events_space', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('country', self.gf('django.db.models.fields.CharField')(default='US', max_length=50)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('lon', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('photo', self.gf('django.db.models.fields.files.FileField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal(u'events', ['Space'])

        # Adding model 'Event'
        db.create_table(u'events_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('bulk_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=120, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('space', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='events_hosted', null=True, on_delete=models.SET_NULL, to=orm['events.Space'])),
        ))
        db.send_create_signal(u'events', ['Event'])

        # Adding index on 'Event', fields ['title', 'start', 'end']
        db.create_index(u'events_event', ['title', 'start', 'end'])

        # Adding M2M table for field areas on 'Event'
        m2m_table_name = db.shorten_name(u'events_event_areas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'events.event'], null=False)),
            ('functionalarea', models.ForeignKey(orm[u'events.functionalarea'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'functionalarea_id'])


    def backwards(self, orm):
        # Removing index on 'Event', fields ['title', 'start', 'end']
        db.delete_index(u'events_event', ['title', 'start', 'end'])

        # Deleting model 'FunctionalArea'
        db.delete_table(u'events_functionalarea')

        # Deleting model 'Space'
        db.delete_table(u'events_space')

        # Deleting model 'Event'
        db.delete_table(u'events_event')

        # Removing M2M table for field areas on 'Event'
        db.delete_table(db.shorten_name(u'events_event_areas'))


    models = {
        u'events.event': {
            'Meta': {'object_name': 'Event', 'index_together': "[['title', 'start', 'end']]"},
            'areas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['events.FunctionalArea']", 'symmetrical': 'False', 'blank': 'True'}),
            'bulk_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120', 'blank': 'True'}),
            'space': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events_hosted'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['events.Space']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'events.functionalarea': {
            'Meta': {'object_name': 'FunctionalArea'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'red-1'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'events.space': {
            'Meta': {'object_name': 'Space'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'US'", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['events']