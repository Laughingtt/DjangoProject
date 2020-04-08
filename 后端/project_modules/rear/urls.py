from django.urls import path
from . import views

app_name = 'rear'

urlpatterns = [
    path('',views.index,name='index'),
    path('look/',views.look,name='look'),
    path('update/',views.update,name='update'),
    path('find/',views.find,name='find'),
]