from django.shortcuts import render
import datetime
from operator import attrgetter

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .classes import IncomeMetric, Order
from .forms import PassengerInfoForm, UserForm
from .models import Flight, Route

ADMIN_ID = 3  # 管理员ID为3


def admin_dashboard(request):
    all_routes = Route.objects.all()
    all_routes = sorted(all_routes,
                        key=attrgetter('leave_time'))  # 将所有航班按照起飞时间排序
    # 将航班每天的收入打上不同的时间标签 [周，月，日]
    week_day_incomes = []
    month_day_incomes = []
    year_day_incomes = []

    # 用set存储所有的 周，月，年
    week_set = set()
    month_set = set()
    year_set = set()
    for route in all_routes:
        if route.income > 0:  # 只统计有收入的航班
            # 打上周标签
            this_week = route.leave_time.strftime('%W')  # datetime获取周
            week_day_incomes.append(
                (this_week, route.income))  # 添加元组(week, income)
            week_set.add(this_week)
            # 打上月标签
            this_month = route.leave_time.strftime('%m')  # datetime获取月
            month_day_incomes.append(
                (this_month, route.income))  # 添加元组(month, income)
            month_set.add(this_month)
            # 打上年标签
            this_year = route.leave_time.strftime('%Y')  # datetime获取年
            year_day_incomes.append(
                (this_year, route.income))  # 添加元组(year, income)
            year_set.add(this_year)

    # 存储每周收入
    # 将每周的收入用 IncomeMetric 类型存储在 week_incomes List中
    week_incomes = []
    for week in week_set:
        income = sum(x[1] for x in week_day_incomes
                     if x[0] == week)  # 同周次的income求和
        route_sum = sum(1 for x in week_day_incomes
                        if x[0] == week)  # 同周次的航班总数目
        week_income = IncomeMetric(week, route_sum,
                                   income)  # 将数据存储到IncomeMetric类中
        week_incomes.append(week_income)
    week_incomes = sorted(
        week_incomes, key=attrgetter('metric'))  # 将List类型的 week_incomes 按周次升序排列

    # 存储每月收入
    # 将每月的收入用 IncomeMetric 类型存储在 month_incomes List中
    month_incomes = []
    for month in month_set:
        income = sum(x[1] for x in month_day_incomes if x[0] == month)
        route_sum = sum(1 for x in month_day_incomes if x[0] == month)
        month_income = IncomeMetric(month, route_sum, income)
        month_incomes.append(month_income)
    month_incomes = sorted(
        month_incomes,
        key=attrgetter('metric'))  # 将List类型的 month_incomes 按月份升序排列

    # 存储每年收入
    # 将每年的收入用 IncomeMetric 类型存储在 year_incomes List中
    year_incomes = []
    for year in year_set:
        income = sum(x[1] for x in year_day_incomes if x[0] == year)
        route_sum = sum(1 for x in year_day_incomes if x[0] == year)
        year_income = IncomeMetric(year, route_sum, income)
        year_incomes.append(year_income)
    year_incomes = sorted(
        year_incomes, key=attrgetter('metric'))  # 将List类型的 year_incomes 按年份升序排列

    # 存储订单信息
    # 外层循环查找所有乘客，内层查找所有乘客的所有航班，最后单独记录为一个订单Set存储
    passengers = User.objects.exclude(pk=3)  # 去掉管理员
    order_set = set()
    for p in passengers:
        flights = Flight.objects.filter(User=p)
        for f in flights:
            line = f.leave_city + ' → ' + f.arrive_city
            order = Order(p.username, f.name, line, f.leave_time, f.price)
            order_set.add(order)

        # 信息传给前端
    context = {
        'week_incomes': week_incomes,
        'month_incomes': month_incomes,
        'year_incomes': year_incomes,
        'order_set': order_set
    }
    return render(request, 'admin_dashboard.html', context)


# 管理员后台财务管理
# 统计航空公司每周、每月，每年营业收入情况。
def admin_finance(request):
    all_routes = Route.objects.all()
    all_routes = sorted(all_routes,
                        key=attrgetter('leave_time'))  # 将所有航班按照起飞时间排序
    # 将航班每天的收入打上不同的时间标签 [周，月，日]
    week_day_incomes = []
    month_day_incomes = []
    year_day_incomes = []

    # 用set存储所有的 周，月，年
    week_set = set()
    month_set = set()
    year_set = set()
    for route in all_routes:
        if route.income > 0:  # 只统计有收入的航班
            # 打上周标签
            this_week = route.leave_time.strftime('%W')  # datetime获取周
            week_day_incomes.append(
                (this_week, route.income))  # 添加元组(week, income)
            week_set.add(this_week)
            # 打上月标签
            this_month = route.leave_time.strftime('%m')  # datetime获取月
            month_day_incomes.append(
                (this_month, route.income))  # 添加元组(month, income)
            month_set.add(this_month)
            # 打上年标签
            this_year = route.leave_time.strftime('%Y')  # datetime获取年
            year_day_incomes.append(
                (this_year, route.income))  # 添加元组(year, income)
            year_set.add(this_year)

    # 存储每周收入
    # 将每周的收入用 IncomeMetric 类型存储在 week_incomes List中
    week_incomes = []
    for week in week_set:
        income = sum(x[1] for x in week_day_incomes
                     if x[0] == week)  # 同周次的income求和
        route_sum = sum(1 for x in week_day_incomes
                        if x[0] == week)  # 同周次的航班总数目
        week_income = IncomeMetric(week, route_sum,
                                   income)  # 将数据存储到IncomeMetric类中
        week_incomes.append(week_income)
    week_incomes = sorted(
        week_incomes, key=attrgetter('metric'))  # 将List类型的 week_incomes 按周次升序排列

    # 存储每月收入
    # 将每月的收入用 IncomeMetric 类型存储在 month_incomes List中
    month_incomes = []
    for month in month_set:
        income = sum(x[1] for x in month_day_incomes if x[0] == month)
        route_sum = sum(1 for x in month_day_incomes if x[0] == month)
        month_income = IncomeMetric(month, route_sum, income)
        month_incomes.append(month_income)
    month_incomes = sorted(
        month_incomes,
        key=attrgetter('metric'))  # 将List类型的 month_incomes 按月份升序排列

    # 存储每年收入
    # 将每年的收入用 IncomeMetric 类型存储在 year_incomes List中
    year_incomes = []
    for year in year_set:
        income = sum(x[1] for x in year_day_incomes if x[0] == year)
        route_sum = sum(1 for x in year_day_incomes if x[0] == year)
        year_income = IncomeMetric(year, route_sum, income)
        year_incomes.append(year_income)
    year_incomes = sorted(
        year_incomes, key=attrgetter('metric'))  # 将List类型的 year_incomes 按年份升序排列

    # 存储订单信息
    # 外层循环查找所有乘客，内层查找所有乘客的所有航班，最后单独记录为一个订单Set存储
    passengers = User.objects.exclude(pk=3)  # 去掉管理员
    order_set = set()
    for p in passengers:
        flights = Flight.objects.filter(User=p)
        for f in flights:
            line = f.leave_city + ' → ' + f.arrive_city
            order = Order(p.username, f.name, line, f.leave_time, f.price)
            order_set.add(order)

        # 信息传给前端
    context = {
        'week_incomes': week_incomes,
        'month_incomes': month_incomes,
        'year_incomes': year_incomes,
        'order_set': order_set
    }
    return context


# 显示用户订单信息
# 航班信息，退票管理
def user_info(request):
    if request.user.is_authenticated:
        # 如果用户是管理员，render公司航班收入统计信息页面 admin_finance
        if request.user.id == ADMIN_ID:
            context = admin_finance(request)  # 获取传入的前端数据
            return render(request, 'admin_finance.html', context)
        # 如果用户是普通用户，render用户的机票信息 user_info
        else:
            booked_flights = Flight.objects.filter(User=request.user)  # 从 booksystem_flight_user 表过滤出该用户订的航班，大写
            context = {
                'booked_flights': booked_flights,
                'username': request.user.username,  # 导航栏信息更新
            }
            return render(request, 'user_info.html', context)
    return render(request, 'login.html')  # 用户如果没登录，render登录页面


# 主页
# 欢迎页面性质的订票页面
def index(request):
    return render(request, 'index.html')


# 欢迎页面性质的订票查询页面
def mainmenu(request):
    return render(request, 'mainmenu.html')


# 免除csrf
@csrf_exempt
def book_ticket(request, flight_id):
    if not request.user.is_authenticated:  # 如果没登录就render登录页面
        return render(request, 'login.html')
    else:
        flight = Flight.objects.get(pk=flight_id)
        # 查看乘客已经订购的flights
        booked_flights = Flight.objects.filter(User=request.user)  # 返回 QuerySet
        if flight in booked_flights:
            return render(request, 'book_conflict.html')
        # 查看已经被其他人预订的航班
        others_flights = Flight.objects.filter(User__isnull=False)
        if flight in others_flights:
            return render(request, 'book_conflict.html')

        # book_flight.html 点确认之后，request为 POST 方法，虽然没有传递什么值，但是传递了 POST 信号
        # 确认订票，flight数据库改变
        route = Route.objects.get(pk=flight.Route_id)
        # 找到所有航班下的还没有被人预订的机票数量
        remain_seats = Flight.objects.filter(Route_id=flight.Route_id,
                                             User__isnull=True).count()
        # 验证一下，同样的机票只能订一次
        if request.method == 'POST':
            if route.capacity > 0:
                route.book_sum += 1
                route.income += flight.price
                flight.User.add(request.user)
                flight.save()  # 一定要记着save
                route.save()
        # 传递更改之后的票务信息
        context = {'flight': flight,
                   'username': request.user.username,
                   'route': route,
                   'remain_seats': remain_seats,
                   }
        return render(request, 'book_flight.html', context)


# 退票
def refund_ticket(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    route = Route.objects.get(pk=flight.Route_id)
    route.book_sum -= 1
    route.income -= flight.price
    flight.User.remove(request.user)
    flight.save()
    route.save()
    return HttpResponseRedirect('/booksystem/user_info')


# 改签
def rebook_ticket(request, flight_id):
    # 完成所有退票事宜
    flight = Flight.objects.get(pk=flight_id)
    route = Route.objects.get(pk=flight.Route_id)
    route.book_sum -= 1
    route.income -= flight.price
    flight.User.remove(request.user)
    flight.save()
    route.save()

    # 重新搜索相同起飞城市和到达城市的航班以供乘客选择
    passenger_lcity = flight.leave_city
    passenger_acity = flight.arrive_city
    all_routes = Route.objects.filter(leave_city=passenger_lcity,
                                      arrive_city=passenger_acity,)

    usable_routes = []
    for route in all_routes:  # off-set aware
        usable_routes.append(route)

    # 按不同的key排序
    usable_routes_by_ltime = sorted(
        usable_routes, key=attrgetter('leave_time'))  # 起飞时间从早到晚
    usable_routes_by_atime = sorted(usable_routes,
                                    key=attrgetter('arrive_time'))
    usable_routes_by_capacity = sorted(usable_routes,
                                       key=attrgetter('capacity'))  # 容量从低到高

    # 转换时间格式
    time_format = '%m/%d %H:%M'
    for route in usable_routes_by_capacity:
        route.leave_time = route.leave_time.strftime(
            time_format)  # 转成了str
        route.arrive_time = route.arrive_time.strftime(time_format)

    # 决定 search_head , search_failure 是否显示
    dis_search_head = 'block'
    dis_search_failure = 'none'
    if len(usable_routes_by_capacity) == 0:
        dis_search_head = 'none'
        dis_search_failure = 'block'
    context = {
        # 搜索结果
        'usable_routes_by_ltime': usable_routes_by_ltime,
        'usable_routes_by_atime': usable_routes_by_atime,
        'usable_routes_by_capacity': usable_routes_by_capacity,
        # 标记
        'dis_search_head': dis_search_head,
        'dis_search_failure': dis_search_failure
    }
    if request.user.is_authenticated:  # FIXME: django higher version 'bool' object is not callable
        context['username'] = request.user.username
    return render(request, 'rebook_flight.html',
                  context)  # 最前面如果加了/就变成根目录了，url错误


# 退出登录
def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'login.html', context)


# 登录
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None:  # 登录成功
            if user.is_active:  # 加载订票页面
                login(request, user)
                context = {'username': request.user.username}
                if user.id == ADMIN_ID:
                    context = admin_finance(request)
                    return render(request, 'admin_finance.html', context)
                else:
                    return render(request, 'result.html', context)
            else:
                return render(
                    request, 'login.html',
                    {'error_message': 'Your account has been disabled'})
        else:  # 登录失败
            return render(request, 'login.html',
                          {'error_message': 'Invalid login'})
    return render(request, 'login.html')


# 注册
def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                context = {'username': request.user.username}
                return render(request, 'result.html',
                              context)  # 注册成功直接render result页面
    context = {
        "form": form,
    }
    return render(request, 'register.html', context)


# 搜索结果页面
def result(request):
    if request.method == 'POST':
        form = PassengerInfoForm(request.POST)  # 绑定数据至表单
        if form.is_valid():
            passenger_lcity = form.cleaned_data.get('leave_city')
            passenger_acity = form.cleaned_data.get('arrive_city')
            passenger_ldate = form.cleaned_data.get('leave_date')
            # print(type(passenger_ldate))

            # 全设为naive比较
            # china_tz = pytz.timezone('Asia/Shanghai')
            # passenger_ltime = datetime.datetime(
            #     year=passenger_ldate.year,
            #     month=passenger_ldate.month,
            #     day=passenger_ldate.day,
            #     hour=0, minute=0, second=0,
            #     tzinfo=china_tz
            # )

            # 全设为aware比较
            passenger_ltime = datetime.datetime.combine(passenger_ldate,
                                                        datetime.time())
            print(passenger_ltime)

            # filter 可用航班route
            all_routes = Route.objects.filter(leave_city=passenger_lcity,
                                              arrive_city=passenger_acity)
            usable_routes = []
            for route in all_routes:  # off-set aware
                # replace方法必须要赋值。。笑哭
                route.leave_time = route.leave_time.replace(tzinfo=None)
                # 只查找当天的航班
                if route.leave_time.date() == passenger_ltime.date():
                    usable_routes.append(route)

            # 按不同的key排序
            usable_routes_by_ltime = sorted(
                usable_routes, key=attrgetter('leave_time'))  # 起飞时间从早到晚
            usable_routes_by_atime = sorted(usable_routes,
                                            key=attrgetter('arrive_time'))
            usable_routes_by_capacity = sorted(usable_routes,
                                               key=attrgetter('capacity'))  # 容量从低到高

            # 转换时间格式
            time_format = '%H:%M'
            for route in usable_routes_by_capacity:
                route.leave_time = route.leave_time.strftime(
                    time_format)  # 转成了str
                route.arrive_time = route.arrive_time.strftime(time_format)

            # 决定 search_head , search_failure 是否显示
            dis_search_head = 'block'
            dis_search_failure = 'none'
            if len(usable_routes_by_capacity) == 0:
                dis_search_head = 'none'
                dis_search_failure = 'block'
            context = {
                # 搜多框数据
                'leave_city': passenger_lcity,
                'arrive_city': passenger_acity,
                'leave_date': str(passenger_ldate),
                # 搜索结果
                'usable_routes_by_ltime': usable_routes_by_ltime,
                'usable_routes_by_atime': usable_routes_by_atime,
                'usable_routes_by_capacity': usable_routes_by_capacity,
                # 标记
                'dis_search_head': dis_search_head,
                'dis_search_failure': dis_search_failure
            }
            if request.user.is_authenticated:  # FIXME: django higher version 'bool' object is not callable
                context['username'] = request.user.username
            return render(request, 'result.html',
                          context)  # 最前面如果加了/就变成根目录了，url错误
        else:
            return render(
                request, 'mainmenu.html')  # 在index界面提交的表单无效，就保持在index界面
    else:
        context = {'dis_search_head': 'none', 'dis_search_failure': 'none'}
    return render(request, 'result.html', context)


# 选座页面
def book_seats(request, route_id):
    if not request.user.is_authenticated:  # 如果没登录就render登录页面
        return render(request, 'login.html')
    else:
        all_flights = Flight.objects.filter(Route_id=route_id)  # 通过外码筛选出当前航线所有的机票
        time_format = '%H:%M'
        for flight in all_flights:
            flight.leave_time = flight.leave_time.strftime(
                time_format)  # 转成了str
            flight.arrive_time = flight.arrive_time.strftime(time_format)
        usable_flights = []
        for flight in all_flights:
            usable_flights.append(flight)

        # 按不同的key排序
        usable_flights_by_ltime = sorted(usable_flights,
                                         key=attrgetter('leave_time'))  # 起飞时间从早到晚
        usable_flights_by_atime = sorted(usable_flights,
                                         key=attrgetter('arrive_time'))
        usable_flights_by_price = sorted(usable_flights,
                                         key=attrgetter('price'))  # 价格从低到高

        # 决定 search_head , search_failure 是否显示
        dis_search_head = 'block'
        dis_search_failure = 'none'
        if len(usable_flights_by_price) == 0:
            dis_search_head = 'none'
            dis_search_failure = 'block'
        context = {
            # 搜索结果
            'usable_flights_by_ltime': usable_flights_by_ltime,
            'usable_flights_by_atime': usable_flights_by_atime,
            'usable_flights_by_price': usable_flights_by_price,
            # 标记
            'dis_search_head': dis_search_head,
            'dis_search_failure': dis_search_failure,
        }
        if request.user.is_authenticated:  # FIXME: django higher version 'bool' object is not callable
            context['username'] = request.user.username
        return render(request, 'book_seats.html',
                      context)  # 最前面如果加了/就变成根目录了，url错误
