from django.shortcuts import render

# Create your views here.
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from apps.devices.models import devices

# 实际列表--------搜素、过滤、分页
from devices.serializers import DevicesListSerializer


class SelfPagenation(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # 每页显示的参数名
    max_page_size = 77
    page_query_param = 'page'  # 分页参数名称




class DevicesListView(ListAPIView):
    queryset = devices.objects.all()
    serializer_class = DevicesListSerializer
    pagination_class = SelfPagenation  # 分页
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    # 排序
    ordering_fields = ('device_id', 'device_type')
    ordering = ('-device_id',)  # 默认排序

    # 搜索
    search_fields = ('device_id','device_type')


