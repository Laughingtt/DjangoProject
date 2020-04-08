from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def index(request):
#     a,b,c = '','',''
#     # if request.method == "POST":
#     #     a = request.POST.get('a')
#     #     b = request.POST.get('b')
#     #     c = int(a)+int(b)
#     return render(request,'index.html')
#
#

def index(request):
    return render(request, 'index.html')

import json
def calc(request):
    print(request.POST)
    i1 = int(request.POST.get('i1'))
    i2 = int(request.POST.get('i2'))

    i3 = i1 + i2
    dic={"user":"tian","pwd":"123"}
    return HttpResponse(json.dumps(dic))


def ajax_test(request):
    user_name = request.POST.get("user")
    password = request.POST.get("password")
    print(user_name, password)

    return HttpResponse("OK")
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path=os.path.join(BASE_DIR,'files')
def upload(request):
    if request.method =="POST":
        f1 = request.FILES.get('f1')
        with open(os.path.join(path,f1.name),'wb') as f:
            for i in f1:
                f.write(i)
        print("上传成功")
        return HttpResponse("上传成功")
    return render(request,'upload.html')


def upload_ajax(request):
    if request.is_ajax():
        f1 = request.FILES.get('f1')
        with open(os.path.join(path,f1.name),'wb') as f:
            for i in f1:
                f.write(i)
        print("上传成功")
        return HttpResponse("上传成功")
    return render(request,'upload_ajax.html')
from app01 import models


def reg(request):
    return render(request,'reg.html')

def check(request):
    # p=models.User()
    # p.user="jian"
    # p.password="456"
    # p.save()
    # obj = models.User.objects.all().values()
    print(request.POST)
    if request.is_ajax():
        user = request.POST.get('user')
        obj = models.User.objects.filter(user=user)
        if obj:
            return HttpResponse("用户已存在")
        else:
            return HttpResponse("你可以使用这个用户")
    return HttpResponse("OK")

from django.views import View
from django.http import JsonResponse
class Login(View):

    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        print(request.POST)
        ret = {'status':0,'msg':''}
        user = request.POST.get('user')
        password = request.POST.get('password')
        obj = models.User.objects.filter(user=user,password=password)
        if obj:
            ret['status']=200
            ret['msg']="登录成功"
            ret['url']="/reg/"
            return JsonResponse(ret)
        else:
            ret['status'] = 201
            ret['msg'] = "用户或者密码错误"
            return JsonResponse(ret)