# Generated by Django 3.1.2 on 2021-02-04 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mrs', '0005_auto_20210204_1131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='un_locale',
            new_name='un_code',
        ),
    ]
