# Generated by Django 2.2 on 2021-07-07 22:30

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
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('username', models.CharField(max_length=10, verbose_name='用户名')),
                ('token', models.CharField(max_length=50, verbose_name='通信token')),
                ('openid', models.CharField(max_length=50, verbose_name='公开的ID')),
                ('authority', models.IntegerField(default=0, verbose_name='特权说明')),
                ('user', models.ForeignKey(auto_created=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='用户ID')),
            ],
        ),
    ]
