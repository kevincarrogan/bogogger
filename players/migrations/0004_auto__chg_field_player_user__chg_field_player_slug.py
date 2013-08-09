# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Player.user'
        db.alter_column(u'players_player', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['authorisation.User'], null=True))

        # Changing field 'Player.slug'
        db.alter_column(u'players_player', 'slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from='fullname'))

    def backwards(self, orm):

        # Changing field 'Player.user'
        db.alter_column(u'players_player', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True))

        # Changing field 'Player.slug'
        db.alter_column(u'players_player', 'slug', self.gf('autoslug.fields.AutoSlugField')(max_length=50, unique_with=(), populate_from=None))

    models = {
        u'authorisation.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        u'players.player': {
            'Meta': {'object_name': 'Player'},
            '_first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            '_last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'fullname'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authorisation.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['players']