# Generated by Django 2.2 on 2021-07-06 14:37

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Apptime', models.DateTimeField(default=datetime.datetime.now, verbose_name='日志添加时间')),
                ('log_type', models.CharField(max_length=10, verbose_name='日志类型')),
                ('log_content', models.CharField(max_length=233, verbose_name='日志内容')),
                ('log_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
