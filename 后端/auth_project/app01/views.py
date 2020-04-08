from django.shortcuts import render,HttpResponse,redirect,reverse
from django.contrib import auth
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app01.forms import Reg,Login

def index(request):
    login_obj=Login()
    info=''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = auth.authenticate(request,username=username,password=password)
        print(obj)
        if obj:
            info="登录成功"
            login(request,obj)
            return redirect(reverse('first'))
        else:
            info="登录失败,账号或者密码错误"

            # User.objects.create_user(username=username,password=password)
    return render(request,'index.html',context={"info":info,"login_obj":login_obj})

@login_required
def first(reqeust):
    return render(reqeust,'first.html')


def logout_function(request):
    logout(request)

    return redirect(reverse('index'))

def register(request):
    form_obj = Reg()
    if request.method == "POST":
        form_obj = Reg(request.POST)
        if form_obj.is_valid():
            username=form_obj.cleaned_data['username']
            password=form_obj.cleaned_data['password']
            User.objects.create_user(username=username,password=password)
            print("注册成功")
            return redirect(reverse('index'))

    return render(request,'register.html',context={"form_obj":form_obj})

@login_required
def change_pwd(request):
    error=''
    if request.method=="POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        print(old_password)
        ok = request.user.check_password(old_password)
        if ok:
            print("旧密码正确")
            error="旧密码正确"
            if new_password:
                if new_password == confirm_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    print("修改密码成功")
                    error="修改密码成功"
                    return redirect(reverse('index'))
                else:
                    print("两次密码不一致")
                    error="两次密码不一致"
            else:
                print("密码不能为空")
                error="密码不能为空"
        else:
            error="旧密码错误"
    return render(request,'change_pwd.html',context={"error":error})