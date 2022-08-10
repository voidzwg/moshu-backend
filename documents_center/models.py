# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Groups(models.Model):
    name = models.CharField(max_length=18)
    unum = models.IntegerField()
    pnum = models.IntegerField()
    profile = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '_groups'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Document(models.Model):
    pid = models.ForeignKey('Projects', models.DO_NOTHING, db_column='pid', blank=True, null=True)
    data = models.TextField()
    name = models.CharField(max_length=100)
    create_time = models.DateTimeField(blank=True, null=True)
    modify_time = models.DateTimeField(blank=True, null=True)
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'document'


class DocumentsCenterFiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    lft = models.PositiveIntegerField()
    rght = models.PositiveIntegerField()
    tree_id = models.PositiveIntegerField()
    level = models.PositiveIntegerField()
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    isfile = models.IntegerField(db_column='isFile')  # Field name made lowercase.
    document = models.ForeignKey(Document, models.DO_NOTHING, db_column='document', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documents_center_files'


class Invite(models.Model):
    inviter = models.IntegerField()
    invitee = models.IntegerField()
    gid = models.IntegerField()
    read = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'invite'


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
    showable = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'projects'


class Prototype(models.Model):
    pid = models.ForeignKey(Projects, models.DO_NOTHING, db_column='pid')
    data = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    create_time = models.DateTimeField(blank=True, null=True)
    modify_time = models.DateTimeField(blank=True, null=True)
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prototype'


class Template(models.Model):
    name = models.CharField(max_length=100)
    data = models.TextField()
    width = models.IntegerField()
    height = models.TextField()

    class Meta:
        managed = False
        db_table = 'template'


class Uml(models.Model):
    pid = models.ForeignKey(Projects, models.DO_NOTHING, db_column='pid')
    data = models.TextField()
    name = models.CharField(max_length=100)
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    modify_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uml'


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


class Files(MPTTModel):
    name = models.CharField(max_length=255, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    isfile = models.IntegerField(db_column='isFile')  # Field name made lowercase.
    document = models.ForeignKey(Document, models.DO_NOTHING, db_column='document', blank=True, null=True)

