# Generated by Django 2.0.6 on 2018-06-29 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('puskesmas_app', '0020_auto_20180629_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasien',
            name='dari_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.DataPemeriksaan'),
        ),
        migrations.AlterField(
            model_name='pasien',
            name='gender',
            field=models.CharField(choices=[('L', 'Laki-laki'), ('l', 'Laki-laki'), ('P', 'Perempuan'), ('p', 'Perempuan'), ('TJ', 'Gak Jelas')], default='TJ', max_length=2),
        ),
        migrations.AlterField(
            model_name='pemeriksaan',
            name='pengukuran_fungsi_paru',
            field=models.CharField(choices=[(None, ''), ('Normal', 'Normal'), ('Buruk', 'Buruk')], max_length=10, null=True),
        ),
    ]