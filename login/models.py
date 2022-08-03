from django.db import models

# Create your models here.
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
