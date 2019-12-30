from django.shortcuts import render,HttpResponse,reverse,redirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def index(request):
    if request.method == 'GET':
        return render(request,'front/index.html')
    else:
        cursor = connection.cursor()
        username=request.POST.get('username')
        password=request.POST.get('password')
        res=cursor.execute("select password from userinfo where username=%s",[username])
        if res != 0:
            db_password=cursor.fetchone()[0] #输出值为元组，所以取第一个值
            if password == db_password:
                return redirect(reverse('front:main'))
            else:
                return render(request, 'front/index.html', context={'error': 'Password Error'})
        else:
            return render(request,'front/index.html',context={'error':'User Not Found'})

def main(request):
    return render(request,'front/main.html')

def search(request):
    cursor=connection.cursor()
    cursor.execute("select id,name from books")
    name=cursor.fetchall()
    return render(request,'front/search.html',context={'name':name})

@csrf_exempt
def detail(request,page):
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute("select * from books where id=%s",[page])
        book=cursor.fetchone()
        return render(request,'front/detail.html',context={'book':book})
    else:
        res=request.POST.get('res')
        if res == 'update':
            cursor = connection.cursor()
            name=request.POST.get('name')
            author=request.POST.get('author')
            content = request.POST.get('content')
            cursor.execute("update books set name=%s,author=%s,content=%s where id=%s",[name,author,content,page])
        elif res == 'delete':
            cursor = connection.cursor()
            cursor.execute("delete from books where id=%s",[page])
        return redirect(reverse('front:search'))

@csrf_exempt
def add(request):
    if request.method == "GET":
        return render(request,'front/add.html')
    else:
        cursor = connection.cursor()
        name = request.POST.get('name')
        author = request.POST.get('author')
        content = request.POST.get('content')
        cursor.execute("insert into books(name,author,content) values(%s,%s,%s)",[name,author,content])
        return render(request, 'front/add.html',context={'msg':'添加成功'})
