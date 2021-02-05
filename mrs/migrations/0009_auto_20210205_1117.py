# Generated by Django 3.1.2 on 2021-02-05 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mrs', '0008_auto_20210205_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='correction',
            field=models.ForeignKey(blank=True, db_column='correctionId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mrs.correction'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='jha_items',
            field=models.ManyToManyField(blank=True, to='mrs.JhaItem'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='notes',
            field=models.ManyToManyField(blank=True, to='mrs.Note'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='parts_required',
            field=models.ManyToManyField(blank=True, to='mrs.Part'),
        ),
    ]
