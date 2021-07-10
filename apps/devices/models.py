from django.contrib.auth.models import User

# Create your models here.
from django.db import models


class devices(models.Model):
    device_id = models.CharField(max_length=10, verbose_name='设备ID')
    device_type = models.IntegerField(verbose_name='设备类型')
    device_name = models.CharField(max_length=20,verbose_name='设备名称',default=None)
    device_situation = models.BooleanField(verbose_name='设备工作状态',default=True)

class devices_model(models.Model):
    device_type = models.IntegerField(verbose_name='设备类型')
    device_name = models.CharField(max_length=100,verbose_name='设备类型文字描述')
