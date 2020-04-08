from django.shortcuts import render,HttpResponse,reverse

# Create your views here.
class Info():
    name='tian'
    age=18
    sex='male'
def index(request):
    from datetime import datetime
    context = {
        'info':{
            'name':'tian',
            'age':18,
            'sex':'male',
            'birthday':datetime.now(),
        }
    }
    # context = {'info':Info()}
    return render(request,"front/index.html",context=context)

def author(request):
    author = request.GET.get('author')
    text = "你输入的书籍作者是%s"%author
    return HttpResponse(text)

def book(request,name):
    text = "你书籍名称是%s"%name
    return HttpResponse(text)

def son(request):
    return render(request,"front/son.html")

def base(request):
    return render(request,"front/base.html")

def book_id(request,book_id):
    text = "你书籍的编号是%s"%book_id
    return HttpResponse(text)

def get_url(request):
    url=reverse('front:author')
    return HttpResponse("拿到的书的id的url是: %s"%url)

# def add(value, arg):
#     """Add the arg to the value."""
#     try:
#         return int(value) + int(arg)
#     except (ValueError, TypeError):
#         try:
#             return value + arg
#         except Exception:
#             return ''


def cut(value, arg):
    """Remove all values of arg from the given string."""
    safe = isinstance(value, SafeData)
    value = value.replace(arg, '')
    if safe and arg != ';':
        return mark_safe(value)
    return value
