# Generated by Django 2.0.6 on 2018-07-01 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puskesmas_app', '0022_auto_20180630_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pemeriksaan',
            name='berat_badan',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pemeriksaan',
            name='diastol',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pemeriksaan',
            name='gula',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pemeriksaan',
            name='kolestrol',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pemeriksaan',
            name='lingkar_perut',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pemeriksaan',
            name='sistol',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pemeriksaan',
            name='tinggi_badan',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pemeriksaan',
            name='trigliserida',
            field=models.IntegerField(null=True),
        ),
    ]