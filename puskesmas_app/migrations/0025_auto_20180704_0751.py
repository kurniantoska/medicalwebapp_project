# Generated by Django 2.0.6 on 2018-07-03 23:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puskesmas_app', '0024_auto_20180703_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demografipenduduk',
            name='tahun',
            field=models.PositiveIntegerField(choices=[(2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018)], unique=True, validators=[django.core.validators.MinValueValidator(2015), django.core.validators.MaxValueValidator(2018)]),
        ),
    ]