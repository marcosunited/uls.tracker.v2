# Generated by Django 3.1.2 on 2020-10-19 00:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(db_column='user_id', primary_key=True, serialize=False)),
                ('firstName', models.CharField(db_column='first_name', max_length=30)),
                ('lastName', models.CharField(db_column='last_name', max_length=30)),
                ('nick_name', models.CharField(db_column='nick_name', max_length=20, unique=True)),
                ('password', models.TextField()),
                ('salt', models.TextField()),
                ('statusId', models.IntegerField(db_column='state_id')),
                ('createdDate', models.FloatField(blank=True, db_column='created', null=True)),
                ('updatedDate', models.FloatField(blank=True, db_column='updated', null=True)),
                ('date_of_birth', models.DateField(blank=True, db_column='date_of_birth', null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(null=True)),
            ],
        ),
    ]
