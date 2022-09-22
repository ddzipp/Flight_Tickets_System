from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'booksystem'  # 添加这个属性，方便jinja语法

urlpatterns = [
    # 注册与登录
    url(r'^$', views.index, name='index'),  # 欢迎页面
    url(r'^dashboard/$', views.admin_dashboard, name='dashboard'),  # 财务管理页面
    url(r'^register/$', views.register, name='register'),  # 注册
    url(r'^login/$', views.login_user, name='login'),  # 登入
    url(r'^logout/$', views.logout_user, name='logout'),  # 登出
    url(r'^mainmenu/$', views.mainmenu, name='mainmenu'),  # 搜索主页
    url(r'^result/$', views.result, name='result'),  # 搜索结果
    url(r'^user_info/$', views.user_info, name='user_info'),  # 个人信息页面
    url(r'^book/route/(?P<route_id>[0-9]+)/$', views.book_seats, name='book_seats'),  # 选座
    url(r'^book/flight/(?P<flight_id>[0-9]+)/$', views.book_ticket, name='book_ticket'),  # 订票
    url(r'^refund/flight/(?P<flight_id>[0-9]+)/$', views.refund_ticket, name='refund_ticket'),  # 退票
    url(r'^rebook/flight/(?P<flight_id>[0-9]+)/$', views.rebook_ticket, name='rebook_ticket'),  # 改签

]
