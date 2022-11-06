# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Advertiser(models.Model):
    uname = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    webname = models.CharField(max_length=20, blank=True, null=True)
    week_count = models.CharField(max_length=100, blank=True, null=True)
    month_count = models.CharField(max_length=500, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    update_count = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'advertiser'
        unique_together = (('uname', 'webname'),)


class Secondhand(models.Model):
    title = models.CharField(max_length=200)
    uname = models.CharField(max_length=100, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    reply_count = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    webname = models.CharField(max_length=20)
    url = models.CharField(max_length=100)
    ext1 = models.CharField(max_length=500, blank=True, null=True)
    ext2 = models.CharField(max_length=500, blank=True, null=True)
    ext3 = models.CharField(max_length=500, blank=True, null=True)
    ext4 = models.CharField(max_length=100, blank=True, null=True)
    ext5 = models.CharField(max_length=100, blank=True, null=True)
    update_count = models.IntegerField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    advertiser = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'secondHand'
        unique_together = (('url', 'title', 'webname'),)


class WordSubscribe(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    time = models.DateTimeField(blank=True, null=True)
    word = models.CharField(max_length=191, blank=True, null=True)
    user = models.CharField(max_length=191, blank=True, null=True)
    sckey = models.CharField(max_length=191, blank=True, null=True)
    counts = models.IntegerField(blank=True, null=True)
    enable = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word_subscribe'
        unique_together = (('sckey', 'word'),)
