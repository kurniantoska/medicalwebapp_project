# Generated by Django 2.0.6 on 2018-06-25 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puskesmas_app', '0015_auto_20180625_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pemeriksaan',
            name='kadar_alkohol_pernapasan',
            field=models.NullBooleanField(choices=[(None, ''), (True, 'Positif'), (False, 'Negatif')]),
        ),
        migrations.AlterField(
            model_name='pemeriksaan',
            name='tes_amfetamin_urin',
            field=models.NullBooleanField(choices=[(None, ''), (True, 'Positif'), (False, 'Negatif')]),
        ),
    ]
