# Generated by Django 2.0.6 on 2018-06-29 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puskesmas_app', '0021_auto_20180629_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasien',
            name='gender',
            field=models.CharField(choices=[('L', 'Laki-laki'), ('l', 'Laki-laki'), ('P', 'Perempuan'), ('p', 'Perempuan'), ('TJ', 'Gak Jelas')], default='TJ', max_length=20),
        ),
    ]
