import time
import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import serializers

from apps.users.models import Users

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'password', 'openid')
        extra_kwargs = {
            'password': {'write_only': True}  # 密码只写
        }

    def create(self, validated_data):
        user = Users(**validated_data)
        # user.set_password(validated_data['password'])
        user.save()
        return user
        # return JsonResponse({'status': 200, 'message': '注册成功', 'data': {
        #     'userName': validated_data['username'],
        #     'openID': validated_data['openid']
        # }})


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}  # 密码只写
        }

    def create(self, validated_data):
        user = Users(**validated_data)
        # user.set_password(validated_data['password'])
        #user.save()
        # return user
        # return JsonResponse({'status': 200, 'message': '注册成功', 'data': {
        #     'userName': validated_data['username'],
        #     'openID': validated_data['openid']
        # }})
        # 查询用户是否在数据库中
        if Users.objects.filter(username=user.username).exists():
            users = Users.objects.get(username=user.username)
            print(user.username, user.password)
            print(users.username, users.password)
            if users.password == user.password:
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

