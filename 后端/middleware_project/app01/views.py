from django.shortcuts import render,HttpResponse,redirect,reverse
from django.views.decorators.csrf import csrf_exempt

#cookie版登录
# @csrf_exempt
# def login(request):
#     if request.method == "POST":
#         user=request.POST.get('user')
#         password=request.POST.get('password')
#         if user=='root' and password=='root':
#             ret = redirect(reverse('app01:index'))
#             ret.set_cookie('verify','pass')
#             return ret
#     return render(request,'login.html')


#cookie在views中
# def index(request):
#     try:
#         ret = request.COOKIES['verify']
#         if ret=="pass":
#             return HttpResponse(ret)
#         else:
#             return render(request, 'login.html')
#     except Exception:
#         return render(request, 'login.html')


@csrf_exempt
def login(request):
    if request.method == "POST":
        user=request.POST.get('user')
        password=request.POST.get('password')
        if user=='root' and password=='root':
            request.session['verify']='pass'
            next = request.GET.get('next')
            new = request.GET.get('new')
            print(new)
            if next:
                return redirect(next)
            else:
                return redirect(reverse('app01:index'))
    return render(request,'login.html')

def index(request):
    return HttpResponse('OK')

def home(request):

    ret = HttpResponse(request.COOKIES.get('csrftoken'))

    ret.set_cookie("home","shanghai")
    return ret