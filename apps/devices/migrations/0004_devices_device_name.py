# Generated by Django 2.2 on 2021-07-10 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_auto_20210710_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='device_name',
            field=models.CharField(default=None, max_length=20, verbose_name='设备名称'),
        ),
    ]
