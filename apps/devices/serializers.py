from rest_framework import serializers

from apps.devices.models import devices
class DevicesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = devices
        fields = ['device_id','device_type','device_name','device_situation']  # 所有
        depth = 2
        # fields=('id','username')#自定义序列化器很繁琐
        extra_kwargs = {
            'device_id': {'read_only': True},
            'device_type': {'read_only': True}
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
