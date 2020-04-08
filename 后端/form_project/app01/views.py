from django.shortcuts import render,HttpResponse,redirect
from app01.forms import User,Login
def register(request):
    error = ''
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if len(user)<6:
            error = "你的用户名字符少于六位"
        else:
            return HttpResponse("注册成功")
    return render(request,'reg.html',context={"error":error})


def register2(request):
    form = User()
    if request.method == "POST":
        form = User(request.POST)
        if form.is_valid():  #去校验数据是否合格
            print(form.cleaned_data['user']) ## cleaned_data  是经过校验的数据
            return HttpResponse("注册成功")
    return render(request,'register2.html',context={"form":form})


def reg_last(request):
    form_obj = Login()
    if request.method == 'POST':
        form_obj = Login(request.POST)
        if form_obj.is_valid():
            # 数据库操作
            return redirect('https://www.baidu.com')
    return render(request,'reg_last_self.html',context={"form_obj":form_obj})