from django.contrib.auth.models import User

# Create your models here.
from django.db import models


class environment(models.Model):
    time_stamp = models.CharField(max_length=13, verbose_name='13位时间戳')
    temperature = models.FloatField(verbose_name='温度')
    humidity = models.FloatField(verbose_name='湿度')
    status = models.IntegerField(max_length=2, verbose_name='状态：状态(后台根据温湿度数据分别判断并返回值，0正常，1温度异常，2湿度异常, 3两个异常)',
                                 choices=((0, "正常"), (1, "温度异常"), (2, "湿度异常"), (3, "两个异常")), default=0)
