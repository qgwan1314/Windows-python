import datetime
import time
from random import random
import hashlib

import jwt
import requests
from django.contrib.auth.hashers import check_password
from django.core.serializers import serialize
from django.shortcuts import render
from django.template.base import Token
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, GenericAPIView
from django.contrib.auth.models import User
from rest_framework.views import APIView

from .serializers import *
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict

from django.contrib.auth import authenticate, login, logout

# headers
headers = {
    'alg': "HS256"  # 声明所使用的算法
}


# Create your views here.
# 用户的注册
class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = Users.objects.all()

    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        pwd = request.data.get("password")
        openid = request.data.get("openid")
        res = {"state_code": 400, "message": None, 'status': False}
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
            print(jwt_token)
            Users.objects.create(username=username, password=pwd, openid=openid, token=jwt_token)
            data['username'] = username
            data['token'] = jwt_token
            data['openid'] = openid
            res['message'] = "success"
            res['data'] = data
            res['status']=True
        else:
            res["message"] = "用户名已存在"
            res["state_code"] = 400
            res['data'] = data
        return JsonResponse(res)


# 用户的登陆


class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer
    queryset = Users.objects.all()

    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = Users.objects.filter(username=username).first()
        res = {"state_code": 400, "message": None, 'status': False}
        data = {"username": None, "token": None}
        if user:
            m = hashlib.md5()
            m.update(password.encode())
            result = Users.objects.get(username=username).password
            if password == result:
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
                print(jwt_token)
                Users.objects.filter(username=username).update(token=jwt_token)
                # user2 = Users.objects.filter(username=username, password=pwd).first()
                print(user.username, user.password)
                # random_str = get_random_str(user.username)
                # res['token'] = random_str#计算token
                # json_data = serialize('json', user)  # str
                # json_data = json.loads(json_data)  # 序列化成json对象
                # user = model_to_dict(user)
                data['username'] = user.username
                data['token'] = jwt_token
                res['message'] = "success"
                res['data'] = data
                res['state_code'] = 200
                res['status']=True
            else:
                res["message"] = "密码错误"
                res["state_code"] = 110
                res['data'] = data
        else:
            res["message"] = "用户名不存在"
            res["state_code"] = 110
            res['data'] = data
        return JsonResponse(res)


# 用户的token登陆


class UserTokenLoginView(CreateAPIView):
    serializer_class = UserTokenLoginSerializer
    queryset = Users.objects.all()

    permission_classes = []

    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        # token = request.data.get("token")
        print(token)
        # token=token.split(' ')[1]
        res = {"state_code": 200, "message": None, 'status': True}
        data = {"username": None, "token": None}
        try:
            jwt_decode = jwt.decode(token, 'wnxhbgxye', algorithms=['HS256'])
            username=jwt_decode['name']
            print("name:" + jwt_decode['name'])

            if Users.objects.filter(token=token).exists():
                user=Users.objects.filter(username=username).first()
                m = hashlib.md5()
                m.update(user.password.encode())
                token_dict = {
                    # 创建过期时间为15min
                    'iat': int((datetime.datetime.now() + datetime.timedelta(days=3)).timestamp()),  # 时间戳
                    'name': user.username  # 自定义的参数
                }
                # 调用jwt库，生成json web token
                jwt_token = jwt.encode(token_dict,  # 有效载体
                                       "wnxhbgxye",  # 进行加密签名的密钥
                                       algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
                                       headers=headers  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
                                       ).decode('ascii')
                print(jwt_token)
                Users.objects.filter(username=user.username).update(token=jwt_token)
                # user2 = Users.objects.filter(username=username, password=pwd).first()
                print(user.username, user.password)
                # random_str = get_random_str(user.username)
                # res['token'] = random_str#计算token
                # json_data = serialize('json', user)  # str
                # json_data = json.loads(json_data)  # 序列化成json对象
                # user = model_to_dict(user)
                data['username'] = user.username
                data['token'] = jwt_token
                res['message'] = "success"
                res['data'] = data
            else:
                res["msg"] = "token已过期"
                res["state_code"] = 110
                res['data'] = data
        except Exception as e:
            res["msg"] = "token不存在"
            res["state_code"] = 110
            res['data'] = data
        return JsonResponse(res)


def Login(request):
    if request.method == 'GET':
        return JsonResponse({'status': False, 'message': '跳转到登陆界面', 'data': {
            'token': None
        }})

    if request.method == 'POST':
        # 如果登录成功，绑定参数到cookie中，set_cookie
        name = request.POST.get('username')  # 接收的是body参数
        password = request.POST.get('password')
        # 查询用户是否在数据库中
        if Users.objects.filter(username=name).exists():
            user = Users.objects.get(username=name)
            print(user.username, user.password)
            print(name, password)
            if password == user.password:
                # ticket = 'agdoajbfjad'
                ticket = user.token
                now_time = int(time.time())
                if not ticket.__contains__('TK'):
                    ticket = 'TK' + ticket + str(now_time)
                # 绑定令牌到cookie里面
                # response = HttpResponse()
                response = JsonResponse({'status': True, 'message': '登陆成功', 'data': {
                    'token': ticket,
                    'username': user.username
                }})
                # max_age 存活时间(秒)
                response.set_cookie('ticket', ticket, max_age=10000)
                # 存在服务端
                user.token = ticket
                user.save()  # 保存
                return response
            else:
                # return HttpResponse('用户密码错误')
                return JsonResponse({'status': False, 'message': '用户密码错误', 'data': {
                    'token': None}})
        else:
            # return HttpResponse('用户不存在')
            #######userss=Users.objects.all().values_list("username", 'openid', 'authority')
            # userss=model_to_dict(userss)
            users = Users.objects.all()
            json_data = serialize('json', users)  # str
            json_data = json.loads(json_data)  # 序列化成json对象
            return JsonResponse({'status': False, 'message': '用户不存在', 'data': {
                # 'token': list(users)
                'token': json_data
            }})


def Register(request):
    if request.method == 'GET':
        return JsonResponse({'False': False, 'message': '跳转到注册界面', 'data': {
            'token': None
        }})

    if request.method == 'POST':
        # 注册
        name = request.POST.get('username')
        password = request.POST.get('password')
        openid = request.POST.get('openid')
        # 查询用户是否在数据库中
        if Users.objects.filter(username=name, openid=openid).exists():
            print(name, openid)
            # return HttpResponse('用户不存在')
            return JsonResponse({'status': False, 'message': '用户已存在', 'data': {
                'token': None
            }})
        else:
            print(name, password, openid)
            # 对密码进行加密
            # password = make_password(password)
            Users.objects.create(username=name, password=password, openid=openid)
            return JsonResponse({'status': True, 'message': '用户注册成功', 'data': {
                'username': name,
                'openid': openid
            }})
