from django.urls import path
from requests import request
from .views import *

app_name = '[login]'

urlpatterns = [
    # 登陆
    path('login/', Login, name='Login'),  # http://127.0.0.1:8000/login/login/
    # 注册
    path('register/', Register, name='register'),
]
