from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import routers
from apps.user import views

from rest_framework_jwt.views import obtain_jwt_token


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^', include(router.urls)),
]

# 将下面的代码直接放在总的urls.py的下面
schema_url_patterns =[
    re_path(r'^', include(router.urls)),
    #jwt登陆认证
    path('api_auth/', obtain_jwt_token),
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
   patterns= schema_url_patterns
)

urlpatterns += [
   # path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]