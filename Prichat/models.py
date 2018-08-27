# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class BitmexPrice(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(blank=True, null=True)
    symbol = models.CharField(max_length=100, blank=True, null=True)
    close = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    foreignnotional = models.BigIntegerField(db_column='foreignNotional', blank=True, null=True)  # Field name made lowercase.
    high = models.IntegerField(blank=True, null=True)
    homenotional = models.DecimalField(db_column='homeNotional', max_digits=20, decimal_places=10, blank=True, null=True)  # Field name made lowercase.
    lastsize = models.IntegerField(db_column='lastSize', blank=True, null=True)  # Field name made lowercase.
    low = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    open = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    trades = models.IntegerField(blank=True, null=True)
    turnover = models.BigIntegerField(blank=True, null=True)
    volume = models.BigIntegerField(blank=True, null=True)
    vwap = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bitmex_price'
        unique_together = (('timestamp', 'symbol'),)


class ChatLogs(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    time = models.DateTimeField(blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    group_name = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)
    group_type = models.CharField(max_length=255, blank=True, null=True)
    content_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat_logs'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'



class WordCount(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    time = models.DateTimeField(blank=True, null=True)
    word = models.CharField(unique=True, max_length=191, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word_count'


class WordCountHourly(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    time = models.DateTimeField(blank=True, null=True)
    word = models.CharField(max_length=191, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    weighted_count = models.DecimalField(max_digits=11, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word_count_hourly'
