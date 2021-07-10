from django.contrib.auth.models import User

# Create your models here.
from django.db import models


class entry_person(models.Model):
    time_stamp = models.CharField(max_length=13,verbose_name='13位时间戳')
    entry_person_id = models.CharField(max_length=10, verbose_name='人员id')
    entry_person_name = models.CharField(max_length=10, verbose_name='人员姓名')
