# Generated by Django 2.2 on 2021-07-07 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0002_logs_log_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='log_content',
            field=models.CharField(max_length=100, verbose_name='日志内容'),
        ),
    ]
