from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework import routers
from apps.users import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
# 别忘了导入 listorders 函数

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# 将下面的代码直接放在总的urls.py的下面
schema_url_patterns = [
    #    re_path(r'^', include(router.urls)),
    # jwt登陆认证
    # path('login/', obtain_jwt_token),
    path('users/', include('apps.users.urls', namespace='users'), name='用户模块'),
    path('login/', include('apps.login.urls', namespace='login'))
]

urlpatterns += schema_url_patterns

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="我的商城 API",
        default_version='v1',
        description="我的商城数据接口页面 \n 用户信息管理、商品管理、商品类型管理、购物车管理、订单管理等",
        terms_of_service="http://www.briup.com",
        contact=openapi.Contact(email="chengzy@briup.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
    patterns=schema_url_patterns
)

urlpatterns += [
    # path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
