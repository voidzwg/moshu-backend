# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=18)
    field_password = models.CharField(db_column='_password', max_length=18)  # Field renamed because it started with '_'.
    avatar = models.CharField(max_length=255)
    name = models.CharField(max_length=18)
    email = models.CharField(max_length=18)
    gnum = models.IntegerField()
    profile = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
