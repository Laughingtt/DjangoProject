from django.db import models
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User
from django.utils.translation import ugettext_lazy as _
# from multiselectfield import MultiSelectField
from django.shortcuts import reverse
from django.utils.safestring import mark_safe  # 将html内容返回到前端时，用此方法

course_choices = (('LinuxL', 'Linux中高级'),
                  ('PythonFullStack', 'Python高级全栈开发'),)

class_type_choices = (('fulltime', '脱产班',),
                      ('online', '网络班'),
                      ('weekend', '周末班',),)

source_type = (('qq', "qq群"),
               ('referral', "内部转介绍"),
               ('website', "官方网站"),
               ('baidu_ads', "百度推广"),
               ('office_direct', "直接上门"),
               ('WoM', "口碑"),
               ('public_class', "公开课"),
               ('website_luffy', "路飞官网"),
               ('others', "其它"),)

enroll_status_choices = (('signed', "已报名"),
                         ('unregistered', "未报名"),
                         ('studying', '学习中'),
                         ('paid_in_full', "学费已交齐"))

seek_status_choices = (('A', '近期无报名计划'), ('B', '1个月内报名'), ('C', '2周内报名'), ('D', '1周内报名'),
                       ('E', '定金'), ('F', '到班'), ('G', '全款'), ('H', '无效'),)
pay_type_choices = (('deposit', "订金/报名费"),
                    ('tuition', "学费"),
                    ('transfer', "转班"),
                    ('dropout', "退学"),
                    ('refund', "退款"),)

attendance_choices = (('checked', "已签到"),
                      ('vacate', "请假"),
                      ('late', "迟到"),
                      ('absence', "缺勤"),
                      ('leave_early', "早退"),)

score_choices = ((100, 'A+'),
                 (90, 'A'),
                 (85, 'B+'),
                 (80, 'B'),
                 (70, 'B-'),
                 (60, 'C+'),
                 (50, 'C'),
                 (40, 'C-'),
                 (0, ' D'),
                 (-1, 'N/A'),
                 (-100, 'COPY'),
                 (-1000, 'FAIL'),)


class Customer(models.Model):
    """
    客户表
    """
    qq = models.CharField('QQ', max_length=64, unique=True, help_text='QQ号必须唯一')
    qq_name = models.CharField('QQ昵称', max_length=64, blank=True, null=True)
    name = models.CharField('姓名', max_length=32, blank=True, null=True, help_text='学员报名后，请改为真实姓名')
    sex_type = (('male', '男'), ('female', '女'))
    sex = models.CharField("性别", choices=sex_type, max_length=16, default='male', blank=True, null=True)
    birthday = models.DateField('出生日期', default=None, help_text="格式yyyy-mm-dd", blank=True, null=True)
    phone = models.BigIntegerField('手机号', blank=True, null=True)
    source = models.CharField('客户来源', max_length=64, choices=source_type, default='qq')
    introduce_from = models.ForeignKey('self', verbose_name="转介绍自学员", blank=True, null=True)
    class_type = models.CharField("班级类型", max_length=64, choices=class_type_choices, default='fulltime')
    customer_note = models.TextField("客户备注", blank=True, null=True, )
    status = models.CharField("状态", choices=enroll_status_choices, max_length=64, default="unregistered",
                              help_text="选择客户此时的状态")
    network_consult_note = models.TextField(blank=True, null=True, verbose_name='网络咨询师咨询内容')
    date = models.DateTimeField("咨询日期", auto_now_add=True)
    last_consult_date = models.DateField("最后跟进日期", auto_now_add=True)
    next_date = models.DateField("预计再次跟进时间", blank=True, null=True)
    network_consultant = models.ForeignKey('UserProfile', blank=True, null=True, verbose_name='咨询师',
                                           related_name='network_consultant')
    consultant = models.ForeignKey('UserProfile', verbose_name="销售", related_name='customers', blank=True, null=True, )
    class_list = models.ManyToManyField('ClassList', verbose_name="已报班级", )

    def __str__(self):
        return str(self.name)

    def show_classes(
            self):  # 可以在models中定义函数，查询方法为 字段.all() 方法，结果为QuerySet值，通过对象可以获得具体值，其中get_course_display()为chhoices中对应的值
        # for i in self.class_list.all():
        #     result = i.get_course_display() + " " + str(i.semester) + " " + str(i.campuses)
        #     print(i.get_course_display())
        #     print(i.semester)
        #     print(i.campuses)
        #     print(result)
        return ' | '.join([str(i) for i in self.class_list.all()])
        # return result

    def show_status(self):
        color_dict = {
            "signed": 'green',
            "unregistered": 'red',
            "studying": 'pink',
            "paid_in_full": 'blue',

        }
        return mark_safe(
            '<span style="background-color: {};color: white;padding: 4px">{}</span>'.format(color_dict[self.status],
                                                                                            self.get_status_display()))

    def enroll_link(self):
        if not self.enrollment_set.exists():
            return mark_safe('<a href="{}">添加报名表</a>'.format(reverse('add_enrolment', args=(self.id,))))
        else:
            return mark_safe('<a href="{}">查看报名表</a>'.format(reverse('enrolment_list', args=(self.id,))))

    class Meta:
        # db_table = 'info'   如果不这样指定，字段名默认为app_name， 而表明默认为app名+类名： [app_name]_info.
        verbose_name = '客户信息'  # verbose_name指定在admin管理界面中显示中文；verbose_name表示单数形式的显示
        verbose_name_plural = "客户信息"  # verbose_name_plural表示复数形式的显示；中文的单数和复数一般不作区别。


class Campuses(models.Model):
    """
    校区表
    """
    name = models.CharField(verbose_name='校区', max_length=64)
    address = models.CharField(verbose_name='详细地址', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '校区信息'
        verbose_name_plural = "校区信息"


class ContractTemplate(models.Model):
    """
    合同模板表
    """
    name = models.CharField("合同名称", max_length=128, unique=True)
    content = models.TextField("合同内容")
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '合同信息'
        verbose_name_plural = "合同信息"


class ClassList(models.Model):
    """
    班级表
    """
    course = models.CharField("课程名称", max_length=64, choices=course_choices)
    semester = models.IntegerField("学期")
    campuses = models.ForeignKey('Campuses', verbose_name="校区")
    price = models.IntegerField("学费", default=10000)
    memo = models.CharField('说明', blank=True, null=True, max_length=100)
    start_date = models.DateField("开班日期")
    graduate_date = models.DateField("结业日期", blank=True, null=True)
    contract = models.ForeignKey('ContractTemplate', verbose_name="选择合同模版", blank=True, null=True)
    teachers = models.ManyToManyField('UserProfile', verbose_name="老师")
    class_type = models.CharField(choices=class_type_choices, max_length=64, verbose_name='班额及类型', blank=True,
                                  null=True)

    class Meta:
        unique_together = ("course", "semester", 'campuses')

        verbose_name = '班级信息'
        verbose_name_plural = "班级信息"

    def show_teachers(self):
        return "|".join([str(i) for i in self.teachers.all()])

    def __str__(self):
        # print(self.get_course_display())
        # return "{}{}({})".format(self.get_course_display(), self.semester, self.campuses)
        return self.get_course_display()


class ConsultRecord(models.Model):
    """
    跟进记录表
    """
    customer = models.ForeignKey('Customer', verbose_name="所咨询客户")
    note = models.TextField(verbose_name="跟进内容...")
    status = models.CharField("跟进状态", max_length=8, choices=seek_status_choices, help_text="选择客户此时的状态")
    consultant = models.ForeignKey("UserProfile", verbose_name="跟进人", related_name='records')
    date = models.DateTimeField("跟进日期", auto_now_add=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)

    class Meta:
        verbose_name = '跟进记录'
        verbose_name_plural = '跟进记录'

    def __str__(self):
        return "{}_{}".format(self.customer, self.get_status_display())


class Enrollment(models.Model):
    """
    报名表
    """

    why_us = models.TextField("为什么报名", max_length=1024, default=None, blank=True, null=True)
    your_expectation = models.TextField("学完想达到的具体期望", max_length=1024, blank=True, null=True)
    contract_agreed = models.BooleanField("我已认真阅读完培训协议并同意全部协议内容", default=False)
    contract_approved = models.BooleanField("审批通过", help_text="在审阅完学员的资料无误后勾选此项,合同即生效", default=False)
    enrolled_date = models.DateTimeField(auto_now_add=True, verbose_name="报名日期")
    memo = models.TextField('备注', blank=True, null=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)
    customer = models.ForeignKey('Customer', verbose_name='客户名称')
    school = models.ForeignKey('Campuses')
    enrolment_class = models.ForeignKey("ClassList", verbose_name="所报班级")

    class Meta:
        unique_together = ('enrolment_class', 'customer')


class PaymentRecord(models.Model):
    """
    缴费记录表
    """
    pay_type = models.CharField("费用类型", choices=pay_type_choices, max_length=64, default="deposit")
    paid_fee = models.IntegerField("费用数额", default=0)
    note = models.TextField("备注", blank=True, null=True)
    date = models.DateTimeField("交款日期", auto_now_add=True)
    course = models.CharField("课程名", choices=course_choices, max_length=64, blank=True, null=True, default='N/A')
    class_type = models.CharField("班级类型", choices=class_type_choices, max_length=64, blank=True, null=True,
                                  default='N/A')
    enrolment_class = models.ForeignKey('ClassList', verbose_name='所报班级', blank=True, null=True)
    customer = models.ForeignKey('Customer', verbose_name="客户")
    consultant = models.ForeignKey('UserProfile', verbose_name="销售")
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)

    status_choices = (
        (1, '未审核'),
        (2, '已审核'),
    )
    status = models.IntegerField(verbose_name='审核', default=1, choices=status_choices)

    confirm_date = models.DateTimeField(verbose_name="确认日期", null=True, blank=True)
    confirm_user = models.ForeignKey(verbose_name="确认人", to='UserProfile', related_name='confirms', null=True,
                                     blank=True)


class CourseRecord(models.Model):
    """课程记录表"""
    day_num = models.IntegerField("节次", help_text="此处填写第几节课或第几天课程...,必须为数字")
    date = models.DateField(auto_now_add=True, verbose_name="上课日期")
    course_title = models.CharField('本节课程标题', max_length=64, blank=True, null=True)
    course_memo = models.TextField('本节课程内容', max_length=300, blank=True, null=True)
    has_homework = models.BooleanField(default=True, verbose_name="本节有作业")
    homework_title = models.CharField('本节作业标题', max_length=64, blank=True, null=True)
    homework_memo = models.TextField('作业描述', max_length=500, blank=True, null=True)
    scoring_point = models.TextField('得分点', max_length=300, blank=True, null=True)
    re_class = models.ForeignKey('ClassList', verbose_name="班级")
    teacher = models.ForeignKey('UserProfile', verbose_name="讲师")

    class Meta:
        unique_together = ('re_class', 'day_num')

    def __str__(self):
        return str(self.course_title)

class StudyRecord(models.Model):
    """
    学习记录
    """

    attendance = models.CharField("考勤", choices=attendance_choices, default="checked", max_length=64)
    score = models.IntegerField("本节成绩", choices=score_choices, default=-1)
    homework_note = models.CharField(max_length=255, verbose_name='作业批语', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField("备注", max_length=255, blank=True, null=True)
    homework = models.FileField(verbose_name='作业文件', blank=True, null=True, default=None)
    course_record = models.ForeignKey('CourseRecord', verbose_name="某节课程")
    student = models.ForeignKey('Customer', verbose_name="学员")

    class Meta:
        unique_together = ('course_record', 'student')

    def __str__(self):
        return str(self.student)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.normalize_email(username)
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


# A few helper functions for common logic between User and AnonymousUser.
def _user_get_all_permissions(user, obj):
    permissions = set()
    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def _user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_module_perms'):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False


class Department(models.Model):
    name = models.CharField(max_length=32, verbose_name="部门名称")
    count = models.IntegerField(verbose_name="人数", default=0)

    def __str__(self):
        return self.name


class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(
        max_length=255,
        unique=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_admin = models.BooleanField(default=False)
    name = models.CharField('名字', max_length=32)
    department = models.ForeignKey('Department', default=None, blank=True, null=True)
    mobile = models.CharField('手机', max_length=32, default=None, blank=True, null=True)

    memo = models.TextField('备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = '账户信息'
        verbose_name_plural = "账户信息"

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        #     "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always

        if self.is_active and self.is_superuser:
            return True
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        #     "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        #     "Does the user have permissions to view the app `app_label`?"
        #     Simplest possible answer: Yes, always
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    objects = UserManager()
