"""BookingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

import booksystem
from booksystem import views
from django.urls import include, path

urlpatterns = [
    url(r'^booksystem/admin/', admin.site.urls, ),  # 输入admin/会进入django的后台管理页面
    url(r'^booksystem/', include('booksystem.urls', namespace='booksystem')),
    url(r'', include('booksystem.urls', namespace='default')),  # 默认不输入任何url会直接访问Booksystem.urls的文件确定映射路线

]
