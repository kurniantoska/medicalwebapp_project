# Generated by Django 2.0.6 on 2018-06-22 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puskesmas_app', '0007_auto_20180622_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasien',
            name='gender',
            field=models.CharField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan'), ('TJ', 'Gak Jelas')], default='TJ', max_length=2),
        ),
    ]
