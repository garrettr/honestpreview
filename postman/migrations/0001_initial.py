# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MailingList'
        db.create_table('postman_mailinglist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('postman', ['MailingList'])

        # Adding model 'Subscriber'
        db.create_table('postman_subscriber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['postman.MailingList'])),
        ))
        db.send_create_signal('postman', ['Subscriber'])


    def backwards(self, orm):
        
        # Deleting model 'MailingList'
        db.delete_table('postman_mailinglist')

        # Deleting model 'Subscriber'
        db.delete_table('postman_subscriber')


    models = {
        'postman.mailinglist': {
            'Meta': {'object_name': 'MailingList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'postman.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postman.MailingList']"})
        }
    }

    complete_apps = ['postman']
