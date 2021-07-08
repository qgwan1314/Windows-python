from django.contrib.auth.models import User, Group
from rest_framework import serializers


def check_username(username):
    if len(username) < 6:
        raise serializers.ValidationError('不能小于6个字符')
    return username


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_superuser', 'date_joined']  # 所有
        depth = 2
        # fields=('id','username')#自定义序列化器很繁琐
        extra_kwargs = {
            'username': {'read_only': True},
            'date_joined': {'read_only': True}

        }

    # 编辑时加密

    def update(self, instance, validated_data):
        print(validated_data)
        for key, value in validated_data.items():      #字典遍历
            setattr(instance, key, value)#instance：修改对象   instance.user=value
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
