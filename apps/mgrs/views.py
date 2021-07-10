import datetime
import hashlib
import time

import jwt
import requests
from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from requests import Response
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, \
    ListAPIView
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from rest_framework import viewsets, status, filters

from django.contrib.auth import authenticate, login, logout

# Create your views here.
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.users.models import Users
from apps.mgrs.serializers import UsersListSerializer, UserMgrCreateSerializer, UserMgrEditSerializer, \
    UserMgrDelete_Get_Serializer

# headers
headers = {
    'alg': "HS256"  # 声明所使用的算法
}


# Create your views here.
# 新增、用户列表
class UsersSerialView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    # permission_classes = []
    def get(self, request, *args, **kwargs):
        user = request.user
        status = True
        result = {'users': user.username}
        return Response(data=result, status=status)


# 实际列表--------搜素、过滤、分页

class SelfPagenation(PageNumberPagination):
    page_size = 7
    page_size_query_param = 'page_size'  # 每页显示的参数名
    max_page_size = 77
    page_query_param = 'page'  # 分页参数名称


class UsersListView(ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersListSerializer
    pagination_class = SelfPagenation  # 分页
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    # 排序
    ordering_fields = ('user', 'username')
    ordering = ('-username',)  # 默认排序

    # 搜索
    search_fields = ('username','telephone')


# 自定义分页类


class UsersRetrieveUpdateDeleteView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    # permission_classes = []
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    # lookup_url_kwarg = 'pk'
    queryset = Users.objects.all()
    serializer_class = UsersListSerializer
    lookup_url_kwarg = 'pk'


# 添加用户
def add_user(request):
    if request.method == "GET":
        return JsonResponse({'status': True, 'message': '不允许GET', 'data': {
            'token': None
        }})
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        openid = request.POST.get('openid')
        print(username)
        if not Users.objects.filter(username=username).exists():
            Users.objects.create(username=username, password=password, openid=openid)

            return JsonResponse({'status': True, 'message': '用户添加成功', 'data': {
                'token': None
            }})
        else:
            return JsonResponse({'status': False, 'message': '用户名已存在', 'data': {
                'token': None
            }})


# 编辑用户
def edit_user(request):
    if request.method == "GET":
        obj = Users.objects.get(username=request.POST.get('old_username'))
        return JsonResponse({'status': False, 'message': '不容许get请求', 'data': {
            'token': None
        }})
    elif request.method == "POST":
        old_username = request.POST.get('old_username')
        new_username = request.POST.get('new_username')
        password = request.POST.get('password')
        openid = request.POST.get('openid')
        authority = request.POST.get('authority')
        Users.objects.filter(username=old_username).update(username=new_username, password=password, openid=openid,
                                                           authority=authority)

        return JsonResponse({'status': True, 'message': '更改成功', 'data': {
            'token': None
        }})


# 删除用户
def del_user(request):
    Users.objects.filter(username=request.POST.get('username')).delete()

    return JsonResponse({'status': True, 'message': '删除成功', 'data': {
        'token': None
    }})

# API编辑用户
class UserMgrEditView(CreateAPIView):
    serializer_class = UserMgrEditSerializer
    queryset = Users.objects.all()

    permission_classes = []

    # 编辑时加密
    def post(self, request, pk):
        print(pk)
        res = {"state_code": 400, "message": None, 'status': False}
        data = {"username": None, "token": None, "openid": None}
        if Users.objects.filter(id=pk).exists():
            print('存在')
            username = request.data.get("username")
            if not Users.objects.filter(username=username).count()>1:
                password = request.data.get("password")
                openid = request.data.get("openid")
                authority = request.data.get("authority")
                telephone = request.data.get("telephone")
                m = hashlib.md5()
                m.update(password.encode())
                token_dict = {
                    # 创建过期时间为15min
                    'iat': int((datetime.datetime.now() + datetime.timedelta(days=3)).timestamp()),  # 时间戳
                    'name': username  # 自定义的参数
                }
                # 调用jwt库，生成json web token
                jwt_token = jwt.encode(token_dict,  # 有效载体
                                       "wnxhbgxye",  # 进行加密签名的密钥
                                       algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
                                       headers=headers  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
                                       ).decode('ascii')
                # Users.objects.create(username=username, password=pwd, openid=openid, token=jwt_token,user_id=user_id,authority=authority,telephone=telephone)
                Users.objects.filter(id=pk).update(username=username, password=password, openid=openid, telephone=telephone,token=jwt_token,
                                                                   authority=authority)
                data['id'] = pk
                data['username'] = username
                data['token'] = jwt_token
                data['openid'] = openid
                data['authority'] = authority
                data['telephone'] = telephone
                res['message'] = "success"
                res['state_code'] = 200
                res['status'] = True
                res['data'] = data
            else:
                res["message"] = "username已存在"
                res["state_code"] = 400
        else:
            res["message"] = "ID不存在"
            res["state_code"] = 400
        return JsonResponse(res)


# API增加用户
class UserMgrCreateView(CreateAPIView):
    serializer_class = UserMgrCreateSerializer
    queryset = Users.objects.all()

    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        pwd = request.data.get("password")
        openid = request.data.get("openid")
        user_id = request.data.get("user_id")
        authority = request.data.get("authority")
        telephone = request.data.get("telephone")
        res = {"state_code": 200, "message": None, 'status': False}
        data = {"username": None, "token": None, "openid": None}
        if not Users.objects.filter(username=username).exists():
            m = hashlib.md5()
            m.update(pwd.encode())
            token_dict = {
                # 创建过期时间为15min
                'iat': int((datetime.datetime.now() + datetime.timedelta(days=3)).timestamp()),  # 时间戳
                'name': username  # 自定义的参数
            }
            # 调用jwt库，生成json web token
            jwt_token = jwt.encode(token_dict,  # 有效载体
                                   "wnxhbgxye",  # 进行加密签名的密钥
                                   algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
                                   headers=headers  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
                                   ).decode('ascii')
            Users.objects.create(username=username, password=pwd, openid=openid, token=jwt_token,user_id=user_id,authority=authority,telephone=telephone)
            data['user_id'] = user_id
            data['username'] = username
            data['token'] = jwt_token
            data['openid'] = openid
            data['authority'] = authority
            data['telephone'] = telephone
            res['message'] = "success"
            res['state_code'] = 200
            res['status'] = True
            res['data'] = data
        else:
            res["message"] = "用户名已存在"
            res["state_code"] = 110
        return JsonResponse(res)

class UserMgrDelete_Get_View(DestroyAPIView,RetrieveAPIView):
    serializer_class = UserMgrDelete_Get_Serializer
    queryset = Users.objects.all()

    permission_classes = []

    def get(self, request, pk):
        # 查询pk指定的模型对象
        try:
            book = Users.objects.get(id=pk)
        except Users.DoesNotExist:
            return JsonResponse({
                'status':False,
                'message':'id不存在',
                'data':None
            })
        # 创建序列化器进行序列化
        serializer = UserMgrDelete_Get_Serializer(instance=book)
        # 响应
        # return Response(serializer.data)
        return JsonResponse({
            'status': True,
            'message': 'success',
            'data': serializer.data
        })

    def delete(self, request, pk):
        # 查询pk所指定的模型对象
        try:
            book = Users.objects.get(id=pk)
        except Users.DoesNotExist:
             return JsonResponse({
                'status':False,
                'message':'id不存在',
                'data':None
            })

        book.delete()
        return JsonResponse({
            'status': True,
            'message': 'success delete',
            'data': book.username
        })

    # def put(self, request, pk):
    #     # 查询pk所指定的模型对象
    #     try:
    #         book = Users.objects.get(id=pk)
    #     except Users.DoesNotExist:
    #         return JsonResponse({
    #             'status': False,
    #             'message': 'id不存在',
    #             'data': None
    #         })
    #     # 获取前端传入的请求体数据
    #     # 创建序列化器进行反序列化
    #     serializer = UserMgrDelete_Get_Serializer(instance=book, data=request.data)
    #     # 校验
    #     serializer.is_valid(raise_exception=True)
    #     # save--->update
    #     serializer.save()
    #     # 响应
    #     return Response(serializer.data)