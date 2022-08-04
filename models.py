# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Groups(models.Model):
    name = models.CharField(max_length=18)
    unum = models.IntegerField()
    pnum = models.IntegerField()
    profile = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '_groups'

class Document(models.Model):
    pid = models.IntegerField()
    url = models.FileField(max_length=255)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'document'


class Members(models.Model):
    gid = models.ForeignKey(Groups, models.DO_NOTHING, db_column='gid')
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid')
    field_role = models.IntegerField(db_column='_role')  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'members'


class Projects(models.Model):
    name = models.CharField(max_length=18)
    available = models.IntegerField()
    status = models.IntegerField()
    gid = models.ForeignKey(Groups, models.DO_NOTHING, db_column='gid')
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField(blank=True, null=True)
    profile = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projects'


class Prototype(models.Model):
    pid = models.IntegerField()
    url = models.FileField(max_length=255)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'prototype'


class Uml(models.Model):
    pid = models.IntegerField()
    url = models.FileField(max_length=255)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'uml'


class Users(models.Model):
    username = models.CharField(max_length=18)
    field_password = models.CharField(db_column='_password', max_length=18)  # Field renamed because it started with '_'.
    avatar = models.FileField(max_length=255)
    name = models.CharField(max_length=18)
    email = models.CharField(max_length=18)
    gnum = models.IntegerField()
    profile = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
