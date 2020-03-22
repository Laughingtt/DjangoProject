from django.shortcuts import render, HttpResponse, reverse, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from crm.forms import RegForm, CustomerForm, ConsultRecordForm, EnrollmentForm, ClassListForm, CourseRecordForm, \
    StudyRecordForm
from crm import models
from django.utils.safestring import mark_safe  # 安全传输html标签去前端
from script import pagination  # 导入分页类的脚本
from django.views import View
from django.db.models import Q
import copy
from django.http import QueryDict  # request.GET返回的是QueryDict
from django.db import transaction
import time
from django.conf import settings  # 导入自定义setting中的变量
from rbac.server.init_permission import init_permission
from PIL import Image, ImageDraw, ImageFont
import random, os


# 随机生成颜色
def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def v_code(request):
    # img_path = os.path.join(settings.BASE_DIR, 'static/img/')
    # with open(img_path + '1.png', 'wb') as f:
    #     # 创建image对象并调整大小和颜色
    #     img_obj = Image.new('RGB', (250, 35), random_color())
    #
    #     # 在该图片对象上生成一个画笔对象
    #     draw_obj = ImageDraw.Draw(img_obj)
    #
    #     # 将字体导入并设置字体大小
    #     font_obj = ImageFont.truetype('static/font/kumo.ttf', 28)
    #
    #     temp = []
    #     for i in range(5):
    #         l = chr(random.randint(97, 122))  # 小写字母 chr()返回值是当前整数对应的 ASCII 字符。
    #         b = chr(random.randint(65, 90))  # 大写字母
    #         n = str(random.randint(0, 9))
    #
    #         t = random.choice([l, b, n])
    #         temp.append(t)
    #
    #         draw_obj.text((i * 40 + 35, 0), t, fill=random_color(), font=font_obj)
    #
    #     img_obj.save(f)
    # with open('1.png', 'rb') as f:
    #     image_data = f.read()

    # 创建image对象并调整大小和颜色
    img_obj = Image.new('RGB', (250, 35), random_color())

    # 在该图片对象上生成一个画笔对象
    draw_obj = ImageDraw.Draw(img_obj)

    # 将字体导入并设置字体大小
    font_obj = ImageFont.truetype('static/font/kumo.ttf', 28)

    temp = []
    for i in range(5):
        l = chr(random.randint(97, 122))  # 小写字母 chr()返回值是当前整数对应的 ASCII 字符。
        b = chr(random.randint(65, 90))  # 大写字母
        n = str(random.randint(0, 9))

        t = random.choice([l, b, n])
        temp.append(t)

        draw_obj.text((i * 40 + 35, 0), t, fill=random_color(), font=font_obj)

    request.session['v_code'] = ''.join(temp).upper()

    from io import BytesIO
    f1 = BytesIO()
    img_obj.save(f1, format="PNG")
    image_data = f1.getvalue()

    return HttpResponse(image_data, content_type="image/png")


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        v_code = request.POST.get('v_code')
        print(username, password, v_code)
        if v_code.upper() == request.session.get('v_code'):
            ok = auth.authenticate(username=username, password=password)
            if ok:
                auth.login(request, ok)
                init_permission(request, ok)
                return redirect(reverse('customer'))
        else:
            print("验证码错误")

    return render(request, 'login.html')


def register(request):
    form_obj = RegForm()
    if request.method == "POST":
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            print("校验成功")
            form_obj.cleaned_data.pop('re_password')  # 剔除重复的密码
            UserProfile.objects.create_user(**form_obj.cleaned_data)
            return redirect(reverse('login'))

    return render(request, 'register.html', context={"form_obj": form_obj})


@login_required
def index(request):
    return render(request, 'index.html')


def logout(request):
    auth.logout(request)

    return redirect(reverse('login'))


def change_pwd(request):
    error = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        re_new_password = request.POST.get('re_new_password')
        ok = auth.authenticate(username=username, password=password)
        print(request)
        if ok:
            auth.login(request, ok)
            print("原账户密码正确")
            if new_password:
                print("密码不是空")
                if new_password == re_new_password:
                    print("两次密码一致")
                    request.user.set_password(new_password)
                    request.user.save()
                    return redirect(reverse('login'))
                else:
                    error = "两次密码不一致"

            else:
                error = "密码不能为空"
        else:
            error = "原账户或密码不正确"

    return render(request, 'change_pwd.html', context={"error": error})


# FBV写出的视图函数
# def customer(request):
# all_customer = models.Customer.objects.all()
# page_obj = pagination.Page(request, len(all_customer))
# pre = page_obj.pre()
# next = page_obj.next()
# html_str = page_obj.get_html  # 使用了装饰器
# return render(request, 'crm/customer.html',
#               context={"all_customer": all_customer[pre:next], "html_str": html_str})
# CBV写出视图函数
class Show_Customer(View):

    def get(self, request, ret=None):
        # print(request.GET)
        q = self.get_search_contion(['qq', 'name', 'qq_name', 'last_consult_date'])
        if request.path_info == "/crm/":
            all_customer = models.Customer.objects.filter(q, consultant__isnull=True)
        else:
            if request.path_info == "/crm/all_customer/":  # 所有客户
                all_customer = models.Customer.objects.filter(q)
            else:
                all_customer = models.Customer.objects.filter(q, consultant=request.user)  # 我的客户
        query_params = copy.deepcopy(request.GET)  # 深度copy会获取原来的对象再生成一个，不会影响原来的结果
        # print(query_params.urlencode()) #<QueryDict: {'query': ['Laughing'], 'page': ['2']}> 会将QueryDict字典转化为url拼接的方式 query=Laughing&page=2
        len_obj = len(all_customer)
        page_obj = pagination.Page(request, len_obj, query_params)
        pre = page_obj.pre()
        next = page_obj.next()
        html_str = page_obj.get_html  # 使用了装饰器

        add_btn, query_params = self.add_record()
        print(query_params)
        return render(request, 'crm/customer.html',
                      context={"all_customer": all_customer[pre:next], "html_str": html_str, "len_obj": len_obj,
                               "query_params": query_params, "ret": ret})

    def post(self, request):
        # print(request.POST)

        action = request.POST.get('action')
        query = request.POST.get('query')
        if action:
            print(action)
            ret = getattr(self, action)(request)
            print(ret)
            return self.get(request, ret)
        # elif query:  #删除的代码，用post方法实现了查询搜索的功能，但查询后分页功能就会失效，
        #               因为每次点击页面都会发生一个get请求，get请求之后，原有的post查询的数据就会失效，所以还是使用get去实现搜素分页功能
        #     query_params = copy.deepcopy(request.POST)
        #     print(query_params, query_params.urlencode())
        #     query_params._mutable = True
        #     del query_params['csrfmiddlewaretoken']
        #     print(query_params, query_params.urlencode())
        #
        #     ret = self.search(query, query_list=['qq', 'name', 'qq_name', 'last_consult_date'])
        #     return self.get(request, q=ret)
        else:
            return HttpResponse("非法操作")

    def multi_apply(self, request):
        id_list = request.POST.getlist('id')
        # obj = models.Customer.objects.filter(id__in=id_list).update(consultant=request.user)
        # print(settings.MAX_CUSTOMER_NUMBERS)
        if request.user.customers.count() + len(id_list) <= settings.MAX_CUSTOMER_NUMBERS:  # 控制添加客户数量
            with transaction.atomic():  # 添加事务
                obj = models.Customer.objects.filter(id__in=id_list, consultant__isnull=True).select_for_update()  # 加锁，
                if len(id_list) == len(obj):  # 判断，当第一次数量和原本数据量相等时，同意请求
                    time.sleep(1)  # 先申请的的人等待，后申请的人等之前的人
                    obj.update(consultant=request.user)
                    return "客户添加私有成功"
                else:
                    return "客户添加失败"
        else:
            return "超过客户添加上限：5"

    def multi_pub(self, request):
        id_list = request.POST.getlist('id')
        obj = models.Customer.objects.filter(id__in=id_list).update(consultant=None)
        return "客户添加公共成功"

    def multi_delte(self, request):
        id_list = request.POST.getlist('id')
        obj = models.Customer.objects.filter(id__in=id_list).delete()
        return "删除成功"

    def get_search_contion(self, query_list):

        query = self.request.GET.get('query', '')

        q = Q()
        q.connector = 'OR'
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))

        return q

        # Q( Q(qq__contains=query) |  Q(name__contains=query) )

    def add_record(self):
        path = self.request.get_full_path()  # 获得所有页面包括?之后的查询条件
        # url = self.request.path_info        #获得基地址页面
        # print(path, url)
        qd = QueryDict()
        qd._mutable = True
        qd['next'] = path
        # next=%2Fcrm%2Fcustomer_list%2F%3Fquery%3Dalex%26page%3D2
        query_params = qd.urlencode()

        # add_btn = '<a href="{}?next={}" class="btn btn-primary btn-sm">添加</a>'.format(reverse('add_customer'), url)
        add_btn = '<a href="{}?{}" class="btn btn-primary btn-sm">添加</a>'.format(reverse('add_customer'), query_params)

        return mark_safe(add_btn), query_params


# 分页练习
users = [{"name": "tian{0}".format(i), "pwd": "pwd{0}".format(i)} for i in range(302)]


# print(i)
# a={"name":"tian{0}".format(i),"pwd":"pwd{0}".format(i)}
# print(a)
# def page(request):
#     #获取路径
#     path = request.path_info
#     # print(path,request)
#     # 获得当前页码数
#     current = request.GET.get('page', 1)
#     page = int(current)
#     per_pagination = 11  # 显示页码数
#     half = per_pagination // 2
#     per_page = 10  # 每页显示的数据个数
#
#     # 获取当前页应该对应的页面数据
#     pre = (page - 1) * per_page
#     next = page * per_page
#     print(users[pre:next])
#     # 1 0 9
#     # 2 10 19
#     # 3 20 29
#     # 4 30 39
#     # 5 40 49
#
#     # 通过当前页来传递页的数字
#     num_page, remainder = divmod(len(users), per_page)
#     if remainder:
#         num_page += 1
#
#     pagination = [str(i) for i in range(1, num_page + 1)]  # 页码数据列表
#
#     if page > 0 and page < 6:
#         start = 1
#         end = per_pagination
#     elif page > 26:
#         start = num_page - per_pagination + 1
#         end = num_page
#     else:
#         start = page - half
#         end = page + half
#
#     #     # 存放li标签的列表
#     html_list = []
#     #首页
#     first_li = '<li><a href="{}?page=1">首页</a></li>'.format(path)
#     html_list.append(first_li)
#     #上一页
#     if page == 1:
#         prev_li = '<li class="disabled"><a><<</a></li>'
#     else:
#         prev_li = '<li><a href="{1}?page={0}"><<</a></li>'.format((page - 1),path)
#     html_list.append(prev_li)
#     #中间显示页码数
#     for p in pagination[start - 1:end]:
#         page_li = '<li><a href="{1}?page={0}">{0}</a></li>'.format(p,path)
#         html_list.append(page_li)
#     #下一页
#     if page == num_page:
#         next_li = '<li class="disabled"><a>>></a></li>'
#     else:
#         next_li = '<li><a href="{1}?page={0}">>></a></li>'.format((page + 1),path)
#     html_list.append(next_li)
#     #尾页
#     last_li = '<li><a href="{1}?page={0}">尾页</a></li>'.format(num_page,path)
#     html_list.append(last_li)
#
#     html_str = mark_safe(''.join(html_list))
#     return render(request, 'crm/page.html',
#                   context={"users": users[pre:next], "pagination": pagination[start - 1:end], "html_str": html_str}
def page(request):
    page_obj = pagination.Page(request, len(users))
    pre = page_obj.pre()
    next = page_obj.next()
    html_str = page_obj.get_html
    return render(request, 'crm/page.html',
                  context={"users": users[pre:next], "html_str": html_str})


# 增加客户
def add_customer(request):
    customer_obj = CustomerForm()
    if request.method == "POST":
        customer_obj = CustomerForm(request.POST)
        if customer_obj.is_valid():
            customer_obj.save()
            # save方法直接将清洗过的数据存放到数据库中
            print(customer_obj.cleaned_data)

            # 获取到next
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect(reverse('customer'))
    return render(request, 'crm/add_customer.html', context={"customer_obj": customer_obj})


# 编辑客户
def edit_customer(request, customer_id):
    # 参数是通过前端编辑a标签传递customer_id，用id来获取当前信息，并通过form表单实例化，修改完之后再保存下来
    obj = models.Customer.objects.filter(id=customer_id).first()
    customer_obj = CustomerForm(instance=obj)
    if request.method == "POST":
        customer_obj = CustomerForm(request.POST, instance=obj)
        if customer_obj.is_valid():
            customer_obj.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect(reverse('customer'))
    return render(request, 'crm/edit_customer.html', context={"customer_obj": customer_obj})


# 我的客户
def my_customer(request):
    print(request.user)
    obj = models.Customer.objects.filter(consultant=request.user)
    return render(request, 'crm/my_customer.html')


# 测试页面
def test(request):
    customer_obj = CustomerForm()
    print(customer_obj)
    return render(request, 'test.html', {"customer_obj": customer_obj})


##################################################
# 跟进记录函数
class ConsultRecord(View):

    def get(self, request, customer_id):
        q = self.get_search_contion(['customer__name', 'note', 'status', 'consultant__username'])
        print(q)
        if customer_id == '0':
            consult_obj = models.ConsultRecord.objects.filter(q, delete_status=False)
        else:  # 外键的customer的字段名为customer_id
            consult_obj = models.ConsultRecord.objects.filter(q, customer_id=customer_id, delete_status=False)

        query_params = copy.deepcopy(request.GET)
        len_obj = len(consult_obj)
        page_obj = pagination.Page(request, len_obj, query_params)
        pre = page_obj.pre()
        next = page_obj.next()
        html_str = page_obj.get_html  # 使用了装饰器

        query_params = self.add_record()
        return render(request, 'crm/consult_list.html',
                      context={"consult_obj": consult_obj[pre:next], "html_str": html_str, "len_obj": len_obj,
                               "query_params": query_params})

    def post(self, request):
        # print(request.POST)
        action = request.POST.get('action')
        if action:
            print(action)
            ret = getattr(self, action)(request)
            print(ret)
            return self.get(request)
        else:
            return HttpResponse("非法操作")

    # def multi_apply(self, request):
    #     id_list = request.POST.getlist('id')
    #     obj = models.ConsultRecord.objects.filter(id__in=id_list).update(consultant=request.user)
    #     return "客户添加私有成功"
    #
    # def multi_pub(self, request):
    #     id_list = request.POST.getlist('id')
    #     obj = models.ConsultRecord.objects.filter(id__in=id_list).update(consultant=None)
    #     return "客户添加公共成功"

    def multi_delte(self, request):
        id_list = request.POST.getlist('id')
        obj = models.ConsultRecord.objects.filter(id__in=id_list).delete()
        return "删除成功"

    def get_search_contion(self, query_list):

        query = self.request.GET.get('query', '')

        q = Q()
        q.connector = 'OR'
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))

        return q

        # Q( Q(qq__contains=query) |  Q(name__contains=query) )

    def add_record(self):
        path = self.request.get_full_path()  # 获得所有页面包括?之后的查询条件
        qd = QueryDict()
        qd._mutable = True
        qd['next'] = path
        query_params = qd.urlencode()

        add_btn = '<a href="{}?{}" class="btn btn-primary btn-sm">添加</a>'.format(reverse('add_customer'), query_params)

        return query_params


# 增加跟进客户记录
def add_consult(request):
    obj = models.ConsultRecord(consultant=request.user)
    consult_obj = ConsultRecordForm(instance=obj)
    if request.method == "POST":
        consult_obj = ConsultRecordForm(request.POST, instance=obj)
        if consult_obj.is_valid():
            consult_obj.save()
            return redirect(reverse('consult_list', args=(0,)))
    return render(request, 'crm/add_consult.html', context={"consult_obj": consult_obj})


# 编辑跟进客户记录
def edit_consult(request, consult_id):
    obj = models.ConsultRecord.objects.filter(id=consult_id).first()
    consult_obj = ConsultRecordForm(instance=obj)
    if request.method == "POST":
        consult_obj = ConsultRecordForm(request.POST, instance=obj)
        if consult_obj.is_valid():
            consult_obj.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect(reverse('consult_list', args=(0,)))

    return render(request, 'crm/edit_consult.html', context={"consult_obj": consult_obj})


# 新增和编辑跟进记录可以将以上两个函数合并起来
# def consult_record(request, consult_id=None):
#     obj = models.ConsultRecord.objects.filter(id=consult_id).first() or models.ConsultRecord(consultant=request.user)
#     consult_obj = ConsultRecordForm(instance=obj)
#     if request.method == 'POST':
#         consult_obj = ConsultRecordForm(request.POST, instance=obj)
#         if consult_obj.is_valid():
#             consult_obj.save()
#             return redirect(reverse('consult_list',args=(0,)))
#
#     return render(request, 'crm/edit_consult.html', {'consult_obj': consult_obj})

######################################################
# 报名表

class EnrolmentList(View):

    def get(self, request, customer_id):
        q = self.get_search_contion(['why_us', 'your_expectation', 'enrolled_date', 'customer__name'])
        if customer_id == '0':
            enrolment_obj = models.Enrollment.objects.filter(q, delete_status=False)
        else:
            enrolment_obj = models.Enrollment.objects.filter(q, customer_id=customer_id, delete_status=False)

        query_params = copy.deepcopy(request.GET)
        len_obj = len(enrolment_obj)
        page_obj = pagination.Page(request, len_obj, query_params)
        pre = page_obj.pre()
        next = page_obj.next()
        html_str = page_obj.get_html  # 使用了装饰器

        query_params = self.add_record()

        return render(request, 'crm/enrolment_list.html',
                      context={"enrolment_obj": enrolment_obj[pre:next], "html_str": html_str, "len_obj": len_obj,
                               "query_params": query_params})

    def post(self, request, customer_id):
        # print(request.POST)
        action = request.POST.get('action')
        if action:
            print(action)
            ret = getattr(self, action)(request)
            print(ret)
            return self.get(request, customer_id)
        else:
            return HttpResponse("非法操作")

    # def multi_apply(self, request):
    #     id_list = request.POST.getlist('id')
    #     obj = models.ConsultRecord.objects.filter(id__in=id_list).update(consultant=request.user)
    #     return "客户添加私有成功"
    #
    # def multi_pub(self, request):
    #     id_list = request.POST.getlist('id')
    #     obj = models.ConsultRecord.objects.filter(id__in=id_list).update(consultant=None)
    #     return "客户添加公共成功"

    def multi_delte(self, request):
        id_list = request.POST.getlist('id')
        obj = models.Enrollment.objects.filter(id__in=id_list).delete()
        return "删除成功"

    def get_search_contion(self, query_list):

        query = self.request.GET.get('query', '')

        q = Q()
        q.connector = 'OR'
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))

        return q

        # Q( Q(qq__contains=query) |  Q(name__contains=query) )

    def add_record(self):
        path = self.request.get_full_path()  # 获得所有页面包括?之后的查询条件
        qd = QueryDict()
        qd._mutable = True
        qd['next'] = path
        query_params = qd.urlencode()
        return query_params


# 新增报名人员

def add_enrolment(request, customer_id):
    obj = models.Enrollment(customer_id=customer_id)
    form_obj = EnrollmentForm(instance=obj)
    if request.method == "POST":
        form_obj = EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            enrolment_obj = form_obj.save()
            enrolment_obj.customer.status = 'signed'
            enrolment_obj.customer.save()

            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect(reverse('enrolment_list', args=(0,)))
    return render(request, 'crm/add_enrolment.html', context={"form_obj": form_obj})


# 修改报名人员信息
def edit_enrolment(request, enrolment_id):
    obj = models.Enrollment.objects.filter(id=enrolment_id).first()
    form_obj = EnrollmentForm(instance=obj)
    if request.method == "POST":
        form_obj = EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            enrolment_obj = form_obj.save()

            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect(reverse('enrolment_list', args=(0,)))
    return render(request, 'crm/edit_enrolment.html', context={"form_obj": form_obj})


# 班级信息
class ClassList_view(View):

    def get(self, request):
        q = self.get_search_contion(['course', 'semester', 'campuses__name'])
        all_class_obj = models.ClassList.objects.filter(q)

        query_params = copy.deepcopy(request.GET)
        len_obj = len(all_class_obj)
        page_obj = pagination.Page(request, len_obj, query_params)
        pre = page_obj.pre()
        next = page_obj.next()
        html_str = page_obj.get_html  # 使用了装饰器

        query_params = self.add_record()
        return render(request, "crm/class_list.html",
                      context={"all_class_obj": all_class_obj[pre:next], "html_str": html_str, "len_obj": len_obj,
                               "query_params": query_params})

    def post(self, request):
        print(request.POST)
        action = request.POST.get('action')
        if action:
            print(action)
            ret = getattr(self, action)(request)
            print(ret)
            return self.get(request)
        else:
            return HttpResponse("非法操作")

    def multi_delte(self, request):
        id_list = request.POST.getlist('id')
        obj = models.ClassList.objects.filter(id__in=id_list).delete()
        return "删除成功"

    def get_search_contion(self, query_list):
        query = self.request.GET.get('query', '')

        q = Q()
        q.connector = 'OR'
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))

        return q

    def add_record(self):
        path = self.request.get_full_path()  # 获得所有页面包括?之后的查询条件
        qd = QueryDict()
        qd._mutable = True
        qd['next'] = path
        query_params = qd.urlencode()
        return query_params


def add_class_list(request, class_id=None):
    obj = models.ClassList.objects.filter(id=class_id).first()
    class_obj = ClassListForm(instance=obj)
    if request.method == "POST":
        class_obj = ClassListForm(request.POST, instance=obj)
        if class_obj.is_valid():
            class_obj.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('class_list')
    return render(request, 'crm/add_class.html', context={"class_obj": class_obj})


# 课程信息
class CourseList(View):

    def get(self, request, class_id):

        course_obj = models.CourseRecord.objects.filter(re_class_id=class_id)
        return render(request, 'crm/course_list.html', context={"course_obj": course_obj})

    def post(self, request, class_id):  # 当url中有参数时，post也需要传递相同的参数class_id
        print(request.path_info)
        action = request.POST.get('action')
        # action = request.GET
        if action:
            print(action)
            ret = getattr(self, action)(request)
            print(ret)
            return self.get(request, class_id)
        else:
            return HttpResponse("非法操作")

    def multi_delte(self, request):
        id_list = request.POST.getlist('id')
        obj = models.CourseRecord.objects.filter(id__in=id_list).delete()
        return "删除成功"

    def multi_init(self, request):
        # 根据当前提交的课程记录Id批量初识化学生的学习记录

        course_ids = self.request.POST.getlist('id')

        course_obj_list = models.CourseRecord.objects.filter(id__in=course_ids)

        for course_obj in course_obj_list:
            # 查询当前课程记录代表的班级的学生
            all_students = course_obj.re_class.customer_set.filter(status='studying')
            # print(all_students)
            student_list = []

            for student in all_students:
                # models.StudyRecord.objects.create(course_record=course_obj, student=student)

                # obj = models.StudyRecord(course_record=course_obj, student=student)
                # obj.save()

                student_list.append(models.StudyRecord(course_record=course_obj, student=student))

            models.StudyRecord.objects.bulk_create(student_list)


# 新增和编辑函数
def add_course_list(request, course_id=None):
    obj = models.CourseRecord.objects.filter(id=course_id).first()
    course_obj = CourseRecordForm(instance=obj)
    if request.method == "POST":
        course_obj = CourseRecordForm(request.POST, instance=obj)
        if course_obj.is_valid():
            course_obj.save()
            cla_id = request.POST.get('re_class')
            return redirect(reverse('course_list', args=(cla_id,)))
    return render(request, 'crm/add_course_list.html', context={"course_obj": course_obj})


# 学习记录
from django.forms import modelformset_factory


# def StudyList(request, course_id):
#     Formset = modelformset_factory(models.StudyRecord, StudyListForm, extra=0)
#     study_list = models.StudyRecord.objects.filter(course_record_id=course_id)
#     # study_list = models.StudyRecord.objects.all()
#     formset = Formset(queryset=study_list)
#     if request.method == "POST":
#         formset = Formset(request.POST)
#         print(formset.is_valid())
#         if formset.is_valid():
#             formset.save()
#             return redirect(reverse('course_list',args=(course_id,)))
#     return render(request, 'crm/study_list.html', context={"formset": formset})
def study_record(request, course_id):
    print(course_id)
    FormSet = modelformset_factory(models.StudyRecord, StudyRecordForm, extra=0)
    queryset = models.StudyRecord.objects.filter(course_record_id=course_id)
    form_set = FormSet(queryset=queryset)
    if request.method == 'POST':
        form_set = FormSet(request.POST)
        if form_set.is_valid():
            form_set.save()
            return redirect(reverse('study_list', args=(course_id,)))
    return render(request, 'crm/study_list.html', {"form_set": form_set})
