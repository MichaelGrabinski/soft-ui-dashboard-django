
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

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


class HomeItParts(models.Model):
    id = models.BigAutoField(primary_key=True)
    part_id = models.IntegerField(db_column='Part_ID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    location_id = models.IntegerField(db_column='Location_ID')  # Field name made lowercase.
    barcode_rm = models.CharField(db_column='Barcode_Rm', max_length=255)  # Field name made lowercase.
    barcode_add = models.CharField(db_column='Barcode_Add', max_length=255)  # Field name made lowercase.
    qty = models.IntegerField(db_column='Qty')  # Field name made lowercase.
    manufacturer_id = models.IntegerField(db_column='Manufacturer_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HomeItParts'


class ItParts(models.Model):
    part_id = models.AutoField(db_column='PartsID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)
    location_id = models.CharField(db_column='Location_Id',max_length=255, blank=True, null=True)  # Field name made lowercase.
    barcode_rm = models.CharField(db_column='Barcode_Rm', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barcode_add = models.CharField(db_column='Barcode_Add', max_length=255, blank=True, null=True)  # Field name made lowercase.
    qty = models.CharField(db_column='Qty', max_length=255, blank=True, null=True)  # Field name made lowercase.
    manufacturer_id = models.IntegerField(db_column='Manufacturer', blank=True, null=True)  # Field name made lowercase.
    Priority = models.BooleanField(db_column='Priority', blank=True, null=True)
    ShelfID = models.CharField(db_column='ShelfID', max_length=255, blank=True, null=True)

    def serialize(self):
        return {
            'name': self.name,
            'qty': self.qty,
        }

    class Meta:
        managed = False
        db_table = 'ItParts'


class InventoryChange(models.Model):
    part = models.ForeignKey(ItParts, on_delete=models.CASCADE, to_field='part_id', related_query_name='inventory_change', null=True, blank=True)
    user = models.CharField(max_length=255, null=True, blank=True)  # Change this line
    change_type = models.CharField(max_length=255)
    change_value = models.IntegerField(default=0) 
    timestamp = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=255, blank=True, null=True)

    
class Barcode(models.Model):
    barcode = models.CharField(max_length=255, unique=True)
    user = models.CharField(max_length=255)  # Change this line

    def __str__(self):
        return f"{self.user.username} - {self.barcode}"
      
    class Meta:
        managed = True
