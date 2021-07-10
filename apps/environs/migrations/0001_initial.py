# Generated by Django 2.2 on 2021-07-09 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(verbose_name='时间戳')),
                ('temperature', models.CharField(max_length=10, verbose_name='温度')),
                ('humidity', models.CharField(max_length=10, verbose_name='湿度')),
                ('state', models.IntegerField(default=0, verbose_name='状态：状态(后台根据温湿度数据分别判断并返回值，0正常，1温度异常，2湿度异常, 3两个异常)')),
            ],
        ),
    ]
