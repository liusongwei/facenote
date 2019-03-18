"""
Django settings for facenote project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import MongoConn

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xn15$m_59qz5$dnp10jf^u_ynm36xx5#+daheturs&h$_r6xs1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['47.92.165.36', 'www.skinrec.com', '127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'facenote.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'facenote.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MONGODB_CONFIG = {
    'host': '47.92.165.36',
    'port': 27017,
    'db_name': 'test',
    'username': None,
    'password': None,
}

MongoConn.init_conn(MONGODB_CONFIG)
MongoConn.db_index()
res = []
banner = {}
banner['_id'] = 1
banner['image'] = '1.jpg'
banner['url'] = 'www.baidu.com'
res.append(banner)
banner = {}
banner['_id'] = 2
banner['image'] = '2.jpg'
banner['url'] = 'www.baidu.com'
res.append(banner)
banner = {}
banner['_id'] = 3
banner['image'] = '3.jpg'
banner['url'] = 'www.baidu.com'
res.append(banner)
MongoConn.upsert_mary('banner', res)

effect_tags = [
    {
        '_id' : '去细纹',
        'use_count' : 0
    },
    {
        '_id' : '祛黑头',
        'use_count' : 0
    },
    {
        '_id' : '祛痘',
        'use_count' : 0
    },
    {
        '_id' : '收毛孔',
        'use_count' : 0
    },
    {
        '_id' : '补水保湿',
        'use_count' : 0
    },
    {
        '_id' : '祛疤',
        'use_count' : 0
    },
    {
        '_id' : '抗敏感',
        'use_count' : 0
    },
    {
        '_id' : '抗衰老',
        'use_count' : 0
    },
    {
        '_id' : '紧致',
        'use_count' : 0
    },
    {
        '_id' : '抗氧化',
        'use_count' : 0
    },
    {
        '_id' : '缓解毛周角化',
        'use_count' : 0
    },
    {
        '_id' : '清洁',
        'use_count' : 0
    }
]

summary_tags = [
    {
        '_id' : '吃辣',
        'use_count' : 0
    },
    {
        '_id' : '牛羊肉',
        'use_count' : 0
    },
    {
        '_id' : '运动',
        'use_count' : 0
    },
    {
        '_id' : '煲汤喝',
        'use_count' : 0
    },
    {
        '_id' : '油炸食品',
        'use_count' : 0
    },
    {
        '_id' : '无感',
        'use_count' : 0
    },
    {
        '_id' : '熬夜',
        'use_count' : 0
    },
    {
        '_id' : '暴晒',
        'use_count' : 0
    },
    {
        '_id' : '喝酒',
        'use_count' : 0
    },
    {
        '_id' : '香菜',
        'use_count' : 0
    },
    {
        '_id' : '美容spa',
        'use_count' : 0
    },
    {
        '_id' : '未卸妆',
        'use_count' : 0
    },
    {
        '_id' : '过敏',
        'use_count' : 0
    }
]

MongoConn.insert_many('effect_tags', effect_tags)
MongoConn.insert_many('summary_tags', summary_tags)


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "common_static"),
]

#APPID = "wxd1fa6ab7d81d10e7"      # 小程序ID
#SECRET = "d59db949fd967bff0e30b73480edd71e"
APPID = "wxecb7ebcfdcfbb1a0"      # 小程序ID
SECRET = "bffee17d7564e1dc4cea5fe9f7471344"
MCHID = ""      # 商户号
KEY = ""
NOTIFY_URL = ""     # 统一下单后微信回调地址，api demo见notify_view_demo.py



#ERRCODE
OK      = 0
UNKNOWN = -1
UNLOGIN = -2
PARAMERR = -3
PUBLISHLIMIT = -4
