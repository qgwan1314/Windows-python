from django.urls import path
from requests import request
from .views import *

app_name = '[login]'

urlpatterns = [
    # 登陆
    path('login/', UserLoginView.as_view(), name='Login'),  # http://127.0.0.1:8000/login/login/
    # 登陆
    path('tokenlogin/', UserTokenLoginView.as_view(), name='tokenLogin'),  # http://127.0.0.1:8000/login/login/
    # 注册
    path('register/', UserRegisterView.as_view(), name='register'),
]
