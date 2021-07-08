from django.urls import path
from .views import *

app_name = '[users]'#与命名空间一致
from users.apps import *
#user 下的所有路径  启动项目---架子啊settings-----找urls------进行匹配
urlpatterns = [
    path(r'users', UsersSerialView.as_view(), name='users'),
    path('users/<int:pk>', UserRetrieveUpdateDeleteView.as_view(), name='users'),
    path('userlist', UsersListView.as_view(), name='userslist'),#映射视图
]