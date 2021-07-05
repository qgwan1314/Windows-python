"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
#! 1
import sys
sys.path.insert(0,os.path.join(BASE_DIR, 'apps'))
#!
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#&cj9tv+=29frys0)1j9e(19!$lp8#5%+5ls2&n#_-tx##ga5('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

#! 3  注册应用
'rest_framework',
'apps.user',
'apps.logs',
#
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'apps.user',
    'rest_framework',
    'apps.logs',
    'drf_yasg',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "polls/templates")]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myshopdrf',
        'USER':'root',
        'PASSWORD':'root',
        'HOST':'127.0.0.1',
        'PORT':3306
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

#! 5 语言时区
LANGUAGE_CODE = 'zh-hans' # 中文
TIME_ZONE = 'Asia/Shanghai' # 时区配置
USE_TZ = False
#

USE_I18N = True

USE_L10N = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

###################################################################################################################  JWT
REST_FRAMEWORK = {#是一个字典 key-value
		'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': (
        #配置权限
        'rest_framework.permissions.IsAuthenticated',#认证权限：登陆
    ),#元组类型“逗号之重”
    'DEFAULT_AUTHENTICATION_CLASSES': (#认证机制
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

#python manage.py createsuperuser创建管理远远账户

import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',#规定token携带的格式 JWT 空格 TOKEN
    'JWT_ALLOW_REFRESH': True,
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        # 'basic': {
        #         #     'type': 'basic'
        #         # },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'JSON_EDITOR' : True,
    'LOGIN_URL' : 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    'SHOW_REQUEST_HEADERS':True,
    'OPERATIONS_SORTER':'alpah',
    'APIS_SORTER':'alpah',
    'VALIDATOR_URL':None,
}