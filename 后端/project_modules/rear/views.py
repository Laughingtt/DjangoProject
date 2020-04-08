from django.shortcuts import render,HttpResponse,redirect,reverse
from .models import Persons
from django.db import connection
import random,datetime
def index(request):
    #1 for i in range(10):
    #     p=Persons()
    #     p.name=random.choice(['刘备','黄忠'])
    #     p.sex=random.choice(['男','女'])
    #     p.birthday=datetime.datetime.now()
    #     p.save()

    #2 p1=Persons(name='田健',sex='男',birthday='1993-11-14')
    # p1.save()
    #3
    if request.method == "GET":
        return render(request,'rear/index.html')
    else:
        res=request.POST.get('res')
        if res=='ok':
            p=Persons()
            p.name = request.POST.get('name')
            p.sex = request.POST.get('sex')
            p.birthday = request.POST.get('birthday')
            p.save()
            return redirect(reverse('rear:look'))

def look(request):
    # p=Persons.objects.all().values_list()
    # p=Persons.objects.filter(name='黄忠').values_list()
    p=Persons.objects.get(pk=1)
    return render(request,'rear/look.html',context={'p':p})
    # return render(request,'rear/look.html',context={'look':list(p)})

def update(request):
    # p.Person.objects.get(pk=3)
    # p.name='马超'
    # p.save()
    cursor = connection.cursor()
    cursor.execute("desc t1")
    res=cursor.fetchall()
    return HttpResponse(res)
def delete(request):
    p.Person.objects.get(pk=3)
    p.delete()

from .models import *

def foreignkey(request):
   user = User(username="tom",password="tom123")
   user.save()
   article = Article(title="日记",content="今天天气真好")
   article.author = user
   article.save()

   return HttpResponse("succeed")
import datetime
from django.db.models import *
def find(request):
    # user = User.objects.filter(date__date=datetime.date(2020,6,1)).filter(date__date=datetime.date(2020,6,2))
    # user = User.objects.filter(id__isnull=False)
    user = User.objects.all().values_list()
    print(list(user))

    return HttpResponse("succeed")