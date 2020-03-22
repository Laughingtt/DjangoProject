from django.urls import path,re_path
from . import views

app_name = 'front'

urlpatterns = [
    path('',views.index,name='index'),
    path('main/',views.main,name='main'),
    path('main/search/',views.search,name='search'),
    path('main/add/',views.add,name='add'),
    path('main/search/(?P<page>)/',views.detail,name='detail'),

]