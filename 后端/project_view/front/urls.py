from django.urls import path,re_path
from . import views

app_name = 'front'

urlpatterns = [
    path('',views.index,name='index'),
    path('book/author/',views.author,name='author'),
    path('book/<name>/',views.book,name='book_name'),
    re_path('book/(?P<book_id>\d{4})/$',views.book_id,name='book_id'),
    path('book_url/',views.get_url),
    path('son/',views.son,name='son'),
    path('base/',views.base,name='base'),
]

