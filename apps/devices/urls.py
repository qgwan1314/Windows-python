from django.urls import path
from requests import request
from .views import *

app_name = '[devices]'

urlpatterns = [
    # 操作用户
    path(r'deviceslist/', DevicesListView.as_view(), name='deviceslist'),#映射视图

    # path('addusers/', UserMgrCreateView.as_view(), name='add_users'),
    # path(r'editusers/<int:pk>', UserMgrEditView.as_view(), name='edit_users'),
    # path(r'del_get_users/<int:pk>', UserMgrDelete_Get_View.as_view(), name='del_users'),
    # path(r'searchusers/', UserMgrSearchView.as_view(), name='search_users'),
]
