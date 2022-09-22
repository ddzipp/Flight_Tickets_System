from django.db import models

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# login/models.py
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver


class Route(models.Model):
    name = models.CharField(max_length=100)  # 班次  南方航空CZ3969
    leave_city = models.CharField(max_length=100, null=True)  # 离开城市
    arrive_city = models.CharField(max_length=100, null=True)  # 到达城市
    leave_time = models.DateTimeField(
        null=True)  # DateTimeField包括了DateField信息，并且添加了时间
    arrive_time = models.DateTimeField(null=True)
    capacity = models.IntegerField(default=0, null=True)  # 航班座位总数
    book_sum = models.IntegerField(default=0, null=True)  # 订票总人数
    income = models.FloatField(default=0, null=True)  # 收入

    class Meta:
        verbose_name = '航班'
        verbose_name_plural = '航班'

    def __str__(self):
        return self.name


class Flight(models.Model):
    User = models.ManyToManyField(User, default=1)  # 有了这个字段之后，默认的后台添加失效，必须要自定义Form，除去这个字段
    Route = models.ForeignKey(Route, on_delete=models.CASCADE)  # 一个航班可以有多张票，设置外码
    name = models.CharField(max_length=100)  # 班次  南方航空CZ3969
    leave_city = models.CharField(max_length=100, null=True)  # 离开城市
    arrive_city = models.CharField(max_length=100, null=True)  # 到达城市
    leave_airport = models.CharField(max_length=100, null=True)  # 离开的机场
    arrive_airport = models.CharField(max_length=100, null=True)  # 到达的机场
    leave_time = models.DateTimeField(
        null=True)  # DateTimeField包括了DateField信息，并且添加了时间
    arrive_time = models.DateTimeField(null=True)
    row = models.IntegerField(default=0, null=True)  # 座位行
    column = models.CharField(max_length=100, null=True)  # 座位列
    price = models.FloatField(default=0, null=True)  # 价格

    class Meta:
        verbose_name = '机票'
        verbose_name_plural = '机票'

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Flight)
def pre_save_flight(sender, instance, **kwargs):
    route = instance.Route
    route.capacity += 1
    route.save()


@receiver(pre_delete, sender=Flight)
def pre_delete_flight(sender, instance, **kwargs):
    route = instance.Route
    route.capacity -= 1
    route.save()
