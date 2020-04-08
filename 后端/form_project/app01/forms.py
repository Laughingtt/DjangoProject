from django import forms
from django.forms import widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def check(val):
    if "tian" == val:
        raise ValidationError("你输入的用户是错误的")

class User(forms.Form):

    user = forms.CharField(label="用户名",validators=[check])
    pwd = forms.CharField(label="密码")
    gender = forms.fields.ChoiceField(
        choices=((1, "男"), (2, "女"), (3, "保密")),
        label="性别",
        initial=3,
        widget=forms.widgets.RadioSelect()
    )
    hobby = forms.fields.ChoiceField(
        choices=((1, "篮球"), (2, "足球"), (3, "双色球"),),
        label="爱好",
        initial=3,
        widget=forms.widgets.CheckboxSelectMultiple()
    )
    keep = forms.fields.ChoiceField(
        label="是否记住密码",
        initial="checked",
        widget=forms.widgets.CheckboxInput()
    )
    phone = forms.CharField(
        validators=[RegexValidator(r'1[3-9]\d{9}',"手机号不对")]
    )


class Login(forms.Form):

    username = forms.CharField(
        label="用户名"
    )
    password = forms.CharField(
        label='密码',
        min_length=6,
        widget=widgets.PasswordInput()
    )
    re_password = forms.CharField(
        label='确认密码',
        min_length=6,
        widget=widgets.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')

        if pwd == re_pwd:
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError('两次密码不一致')