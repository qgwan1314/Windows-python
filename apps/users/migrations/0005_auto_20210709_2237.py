# Generated by Django 2.2 on 2021-07-09 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210709_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='token',
            field=models.CharField(max_length=255, verbose_name='通信token'),
        ),
    ]
