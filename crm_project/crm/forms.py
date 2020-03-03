from django import forms
from crm import models
from django.core.exceptions import ValidationError


# 注册form
class RegForm(forms.ModelForm):
    password = forms.CharField(
        label='密码',
        widget=forms.widgets.PasswordInput(attrs={'placeholder': '请输入密码'}),
        min_length=6,
        error_messages={'required': '密码不能为空', 'min_length': '最小长度为6'}
    )
    re_password = forms.CharField(
        label='确认密码',
        widget=forms.widgets.PasswordInput(attrs={'placeholder': '请再次确认密码'}),
        min_length=6,
        error_messages={'required': '密码不能为空', 'min_length': '最小长度为6'}
    )

    class Meta:
        model = models.UserProfile
        # fields = '__all__'   # 所有字段
        fields = ['username', 'password', 're_password', 'name', 'department']  # 指定字段
        # exclude = ['']
        widgets = {
            'username': forms.widgets.EmailInput(attrs={'placeholder': '请输入用户名'}),
            'name': forms.widgets.TextInput(attrs={'placeholder': '请输入姓名'}),

        }

        labels = {
            'username': '用户名',
            'password': '密码',
            'name': '姓名',
            'department': '部门',
        }

        error_messages = {
            'username': {
                'required': '账号不能为空',
            },
            'name': {
                'required': '姓名不能为空',
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields.values():
            filed.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd == re_pwd:
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError('两次密码不一致')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'


class ConsultRecordForm(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        exclude = ['delete_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customer_choice = [(i.id, i) for i in self.instance.consultant.customers.all()]
        customer_choice.insert(0, ('', '--------'))
        # 限制客户是当前销售的私户
        self.fields['customer'].widget.choices = customer_choice
        # 限制跟进人是当前的用户（销售） self.instance是传进来的实例化对象
        self.fields['consultant'].widget.choices = [(self.instance.consultant_id, self.instance.consultant), ]


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = models.Enrollment
        exclude = ['delete_status', 'contract_approved']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # # 限制当前的客户只能是传的id对应的客户
        self.fields['customer'].widget.choices = [(self.instance.customer_id, self.instance.customer), ]
        # # 限制当前可报名的班级是当前客户的意向班级
        self.fields['enrolment_class'].widget.choices = [(i.id, i) for i in self.instance.customer.class_list.all()]


class ClassListForm(forms.ModelForm):
    class Meta:
        model = models.ClassList
        fields = '__all__'


class CourseRecordForm(forms.ModelForm):
    class Meta:
        model = models.CourseRecord
        fields = '__all__'


# 学习记录Form
class StudyRecordForm(forms.ModelForm):
    class Meta:
        model = models.StudyRecord
        fields = ['attendance', 'score', 'homework_note', 'student']
