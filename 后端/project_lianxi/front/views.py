from django.shortcuts import render ,reverse,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def index(request,book):
    return render(request,'front/index.html',context={'book':book})
@csrf_exempt
def first(request):
    if request.method=="GET":
        return render(request,'front/first.html')
    else:
        book=request.POST.get('book')
        return redirect(reverse('book',kwargs={'book':book}))