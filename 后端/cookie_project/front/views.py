from django.shortcuts import render,HttpResponse,redirect,reverse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
#写成装饰器来修饰页面
def login_required(fn):
    def inner(request,*args,**kwargs):
        if not request.COOKIES.get('haha') == '1':
            next=request.path_info
            return redirect('/login/?next=%s'%next)
        ret=fn(request,*args,**kwargs)

        return ret
    return inner

@login_required
def index(request):
    return render(request,'index.html')

@login_required
def home(request):
    return render(request,'home.html')

@csrf_exempt
def login(request):
    if request.method == "POST":
        user = request.POST.get('user')
        password = request.POST.get('password')
        # print(user,password)
        if user == 'root' and password =='root':
            next=request.GET.get('next')
            #判断登录前的请求页面也多少，然后登录之后直接跳转过去
            if next:
                ret=redirect(next)
            else:
                ret = redirect(reverse('front:index'))
            ret.set_cookie('haha','1')
            return ret
    else:
        return render(request,'login.html')

#退出登录并删除本次cookie,删除cookie之后，登录记录会消失，退出登录
def logout(request):
    ret = redirect(reverse('front:login'))
    ret.delete_cookie('haha')
    return ret