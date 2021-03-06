# Generated by Django 3.1.2 on 2021-02-05 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mrs', '0007_auto_20210205_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='id_by_project',
            field=models.CharField(db_column='idByProject', max_length=20),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='service_areas',
            field=models.ManyToManyField(blank=True, to='mrs.ServiceArea'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='service_types',
            field=models.ManyToManyField(blank=True, to='mrs.ServiceType'),
        ),
    ]
