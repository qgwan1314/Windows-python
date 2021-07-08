# Create your views here.
import os

from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.users.serializers import *

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status, filters


def get_swagger_docs(filename):
    DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs')
    with open(os.path.join(DIR, filename), 'r', encoding='utf-8') as f:
        return f.read()


user_read_swagger = dict({  # 字典
    'tags': ['用户模块'],
    'operation_summary': '获得用户信息',
    'operation_description': get_swagger_docs('user_read.md')
}, )  # 可以不要后面的参数


@swagger_auto_schema(**user_read_swagger)
def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 新增、用户列表
class UsersSerialView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    # permission_classes = []
    def get(self, request, *args, **kwargs):
        user = request.user
        status = 200
        result = {'users': user.username}
        return Response(data=result, status=status)


# 用户列表--学习用
class UsersListView11(ListAPIView, CreateAPIView):
    # queryset = User.objects.all()
    # queryset = User.objects.filter(is_superuser=1)
    queryset = User.objects.filter()  # 模糊查询username__contains="q"
    # exclude:非管理员  filter:是管理员
    serializer_class = UserListSerializer
    # 序列化转json

    """
        Concrete view for listing a queryset.
        """

    @swagger_auto_schema(**user_read_swagger)  # 接口说明文档
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(**user_read_swagger)
    def post(self, request, *args, **kwargs):
        # 新增操作日志
        user = request.user
        log_ip = request.META.get('HTTP_ORIATATION')
        print(request.user)
        # addlogs(user,"用户管理模块",'新增用户信息',request,log_ip)

        return self.create(request, *args, **kwargs)


# 实际列表--------搜素、过滤、分页

class SelfPagenation(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'  # 每页显示的参数名
    max_page_size = 77
    page_query_param = 'page'  # 分页参数名称


class UsersListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    pagination_class = SelfPagenation#分页
    filter_backends = (filters.OrderingFilter,filters.SearchFilter)
    #排序
    ordering_fields=('id','username')
    ordering=('-id',)#默认排序

    #搜索
    search_fields=('username','email')

#自定义分页类



class UserRetrieveUpdateDeleteView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    # permission_classes = []
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    # lookup_url_kwarg = 'pk'
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    lookup_url_kwarg = 'pk'
