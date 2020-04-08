from django import forms
from django.forms import widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class Reg(forms.Form):

    username = forms.CharField(
        label="用户名",
        min_length=4,
        required=True,
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

class Login(forms.Form):
    username = forms.CharField(
        label="用户名",
        min_length=4,
    )
    password = forms.CharField(
        label='密码',
        min_length=6,
        widget=widgets.PasswordInput()
    )