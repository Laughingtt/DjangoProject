from django.conf.urls import url
from . import views
app_name = 'app01'

urlpatterns = [
    url(r'^login/$',views.login,name='login'),
    url(r'^index/$',views.index,name='index'),
    url(r'^home/$',views.home,name='home'),
]