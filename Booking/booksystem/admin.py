from django.contrib import admin
from .forms import FlightForm
from .models import Flight, Route

admin.site.site_header = '飞机售票管理后台'
admin.site.site_title = '飞机票售票管理后台'


# Register your models here.

# 自定义表单管理
class FlightAdmin(admin.ModelAdmin):
    list_display = ('name', 'leave_airport',
                    'arrive_airport', 'leave_time',
                    'arrive_time', 'row',
                    'column', 'price', 'Route_id')
    form = FlightForm  # 在FlightForm中自定义需要在后台中输入哪些信息
    list_filter = ['price']
    search_fields = ['name']
    ordering = ("id",)


class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'leave_city', 'arrive_city',
                    'leave_time', 'arrive_time', 'capacity',
                    'book_sum', 'income')
    list_filter = ['leave_time']
    search_fields = ['name']
    ordering = ("id",)


# Register your models here.
admin.site.register(Flight, FlightAdmin)
admin.site.register(Route, RouteAdmin)
