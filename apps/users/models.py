from django.contrib.auth.models import User

# Create your models here.
from django.db import models


class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='用户ID',auto_created=True)  # 用户id
    password = models.CharField(max_length=20, verbose_name='密码')
    username = models.CharField(max_length=10, verbose_name='用户名')
    token = models.CharField(max_length=80, verbose_name='通信token')
    openid = models.CharField(max_length=50, verbose_name='公开的ID')
    authority=models.IntegerField(verbose_name='特权说明',default=0)
