from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.

class Logs(models.Model):#对应一张表
    Apptime=models.DateTimeField(verbose_name='日志添加时间',default=datetime.datetime.now)
    log_type=models.CharField(verbose_name='日志类型',max_length=10)
    log_content=models.CharField(verbose_name='日志内容',max_length=100)
    log_ip=models.CharField(verbose_name='访问ip',max_length=20)
    log_id=models.ForeignKey(User,on_delete=models.PROTECT)
