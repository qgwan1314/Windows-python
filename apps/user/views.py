# Create your views here.
import os

from drf_yasg.utils import swagger_auto_schema
from requests import Response

from apps.user.serializers import *

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from apps.user.serializers import UserSerializer, GroupSerializer


def get_swagger_docs(filename):
    DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs')
    with open(os.path.join(DIR, filename),'r',encoding='utf-8') as f:
        return f.read()

user_read_swagger = dict({#字典
    'tags': ['用户模块'],
    'operation_summary':'获得用户信息',
    'operation_description': get_swagger_docs('user_read.md')
},)#可以不要后面的参数

class UserViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    queryset = User.objects.all().order_by('-date_joined')#加入时间倒序
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    允许组查看或编辑的API路径。

    
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@swagger_auto_schema(**user_read_swagger)
def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

