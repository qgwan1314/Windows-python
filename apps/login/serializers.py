import time
import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.template.base import Token
from rest_framework import serializers

from apps.users.models import Users


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'password', 'openid')
        extra_kwargs = {
            'password': {'write_only': True}  # 密码只写
        }

    # def post(self, validated_data):
    #     user = Users(**validated_data)
    #     # user.set_password(validated_data['password'])
    #     user.save()
    #     return user
    #     # return JsonResponse({'status': 200, 'message': '注册成功', 'data': {
    #     #     'userName': validated_data['username'],
    #     #     'openID': validated_data['openid']
    #     # }})


def get_random_str(user):
    import hashlib,time
    ctime=str(time.time())

    md5=hashlib.md5(bytes(user,encoding="utf8"))
    md5.update(bytes(ctime,encoding="utf8"))

    return md5.hexdigest()


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}  # 密码只写
        }
    # def post(self, validated_data):
    #     users = Users(**validated_data)
    #     # user.set_password(validated_data['password'])
    #     users.save()
    #     try:
    #         # 验证用户名或邮箱， Q提供了一个对象间的或（与&）运算
    #         user = Users.objects.get(username=users.username)
    #         ticket = user.token
    #         now_time = int(time.time())
    #         if not ticket.__contains__('TK'):
    #             ticket = 'TK' + ticket + str(now_time)
    #         user.token=ticket
    #         user.refresh_from_db()
    #         # 后台密码为暗文，传入的密码为明文， 所以需要使用check_password()方法验证密码
    #         if user.password==users.password:
    #             return user
    #             # 登陆失败返回None
    #     except Exception as e:
    #         return None
    #     return user


class UserTokenLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('token', )
