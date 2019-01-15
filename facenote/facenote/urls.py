"""facenote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views as login_views
from diary import views as diary_views

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('login/test', login_views.index, name='login_test'),
    path('login', login_views.login, name='login'),
    path('loop_picture', diary_views.get_banner, name='get_banner'),
    path('image/upload', diary_views.upload_pic, name='upload_pic'),
    path('upload_record', diary_views.upload_diary, name='upload_diary'),


]
