# Generated by Django 2.0.6 on 2018-06-28 07:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('puskesmas_app', '0017_auto_20180628_0009'),
    ]

    operations = [
        migrations.AddField(
            model_name='petugaspuskesmas',
            name='user_link',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_link', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='petugaspuskesmas',
            name='puskesmas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='puskesmas', to='puskesmas_app.Puskesmas'),
        ),
    ]