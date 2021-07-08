import time

import requests
from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import *
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse

from django.contrib.auth import authenticate, login, logout


# Create your views here.
# 用户的注册
class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = Users.objects.all()

    permission_classes = []

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# 用户的登陆
class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer
    queryset = Users.objects.filter()

    permission_classes = []

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    # 登录处理
    def signin(self, request, *args, **kwargs):  # self,
        if request.method == 'GET':
            return self

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


                    user.token = ticket
                    user.save()  # 保存
                    return self
                    # return {'status': 200, 'message': '登陆成功', 'data': {
                    #     'token': ticket,
                    #     'username': user.username
                    # }}
                else:
                    return HttpResponse('用户密码错误')
                    # return {'status': 400, 'message': '用户密码错误', 'data': {
                    #     'token': None}}
            else:
                return HttpResponse('用户不存在')
                # {'status': 400, 'message': '用户不存在', 'data': {
                #     'token': None
                # }}


def Login(request):
    if request.method == 'GET':
        return JsonResponse({'status': 400, 'message': '跳转到登陆界面', 'data': {
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
                response = JsonResponse({'status': 200, 'message': '登陆成功', 'data': {
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
                return JsonResponse({'status': 400, 'message': '用户密码错误', 'data': {
                    'token': None}})
        else:
            # return HttpResponse('用户不存在')
            return JsonResponse({'status': 400, 'message': '用户不存在', 'data': {
                'token': None
            }})


def Register(request):
    if request.method == 'GET':
        return JsonResponse({'400': False, 'message': '跳转到注册界面', 'data': {
            'token': None
        }})

    if request.method == 'POST':
        # 注册
        name = request.POST.get('username')
        password = request.POST.get('password')
        openid = request.POST.get('openid')
        # 查询用户是否在数据库中
        if Users.objects.filter(username=name,openid=openid).exists():
            print(name, openid)
            # return HttpResponse('用户不存在')
            return JsonResponse({'status': 400, 'message': '用户已存在', 'data': {
                'token': None
            }})
        else:
            print(name, password,openid)
            # 对密码进行加密
            # password = make_password(password)
            Users.objects.create(username=name, password=password, openid=openid)
            return JsonResponse({'status': 200, 'message': '用户注册成功', 'data': {
                'username': name,
                'openid': openid
            }})
