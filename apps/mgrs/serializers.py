from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from requests import Response
from rest_framework import serializers

from apps.users.models import Users


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','username', 'password', 'token', 'openid', 'authority', 'finger', 'telephone']  # 所有
        depth = 1
        # fields=('id','username')#自定义序列化器很繁琐
        extra_kwargs = {
            'password': {'read_only': True},
            'id': {'read_only': True},
            'username': {'read_only': True}
        }

    # 编辑时加密

    def update(self, instance, validated_data):
        print(validated_data)
        for key, value in validated_data.items():  # 字典遍历
            setattr(instance, key, value)  # instance：修改对象   instance.user=value
        # if 'password' in validated_data:
        #     instance.set_password(validated_data['password'])
        instance.save()
        return instance


# 新增用户
class UserMgrCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user', 'username', 'password', 'openid', 'authority', 'telephone']  # 所有


# 编辑更改用户
class UserMgrEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user','username', 'password', 'openid', 'authority', 'telephone']  # 所有

        depth = 2
        # fields=('id','username')#自定义序列化器很繁琐
        extra_kwargs = {
            'user': {'read_only': True}
        }

    # 编辑时加密
    #
    # def post(self, instance, validated_data):
    #     print(validated_data)
    #     username = validated_data['username']
    #     res = {"state_code": 400, "message": None, 'status': False}
    #     data = {"username": None, "token": None, "openid": None}
    #     if not Users.objects.filter(username=username).exists():
    #         for key, value in validated_data.items():  # 字典遍历
    #             setattr(instance, key, value)  # instance：修改对象   instance.user=value
    #         instance.save()
    #         res['message'] = "success"
    #         res["state_code"] = 200
    #         res['data'] = validated_data
    #         res['status'] = True
    #     else:
    #         res["message"] = "用户名已存在"
    #         res['data'] = validated_data
    #     return JsonResponse(res)
# 获取或删除某个id
class UserMgrDelete_Get_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'  # 所有
        depth = 2
        # fields=('id','username')#自定义序列化器很繁琐
        extra_kwargs = {
            'username': {'read_only': True}
        }
