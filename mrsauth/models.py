from datetime import datetime
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, nick_name, password, **extra_fields):
        if not nick_name:
            raise ValueError('The Email must be set')
        user = self.model(nick_name=nick_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, nick_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('statusId', 1)

        return self.create_user(nick_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, db_column="user_id")
    firstName = models.CharField(max_length=30, db_column="first_name")
    lastName = models.CharField(max_length=30, db_column="last_name")
    nick_name = models.CharField(max_length=20, db_column="nick_name", unique=True)
    password = models.TextField()
    salt = models.TextField()
    authentication_provider = models.CharField(max_length=30, db_column="auth_provider", blank=True, null=True)
    statusId = models.IntegerField(db_column="state_id")
    createdDate = models.FloatField(blank=True, null=True, db_column="created")
    updatedDate = models.FloatField(blank=True, null=True, db_column="updated")

    # Fields inherited from AbstractBaseUser model
    date_of_birth = models.DateField(blank=True, null=True, db_column="date_of_birth")
    picture = models.ImageField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = UserManager()

    def __str__(self):
        return self.nick_name

    USERNAME_FIELD = 'nick_name'
    REQUIRED_FIELDS = ['firstName', 'lastName', ]

    class Meta:
        app_label = 'mrsauth'


class Console(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = 'consoles'


class UsersHistoryLogin(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='userId')
    console = models.ForeignKey(Console, on_delete=models.DO_NOTHING, db_column='consoleId')
    device_imei = models.CharField(db_column='deviceIMEI', max_length=255, blank=True, null=True)
    user_agent = models.CharField(db_column='userAgent', max_length=255, blank=True, null=True)
    position = models.TextField(blank=True, null=True)
    login_datetime = models.DateTimeField(db_column='loginDatetime', default=datetime.now())

    class Meta:
        managed = True
        db_table = 'users_history_logins'
