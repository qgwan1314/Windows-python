from django.urls import path
from requests import request
from .views import *

app_name = '[mgrs]'

urlpatterns = [
    # 操作用户
    path(r'userlist/', UsersListView.as_view(), name='userslist'),#映射视图
    # path(r'adduser/', add_user, name='add_user'),
    # path(r'edituser/', edit_user, name='edit_user'),
    # path(r'deluser/', del_user, name='del_user'),

    path('addusers/', UserMgrCreateView.as_view(), name='add_users'),
    path(r'editusers/<int:pk>', UserMgrEditView.as_view(), name='edit_users'),
    path(r'del_get_users/<int:pk>', UserMgrDelete_Get_View.as_view(), name='del_users'),
    # path(r'searchusers/', UserMgrSearchView.as_view(), name='search_users'),
]
