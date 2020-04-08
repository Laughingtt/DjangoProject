from django.urls import path,re_path
from . import views_session
app_name = "front"

urlpatterns = [
    path(r'index/',views_session.index,name='index'),
    path(r'login/',views_session.login,name='login'),
    path(r'home/',views_session.home,name='home'),
    path(r'logout/',views_session.logout,name='logout'),
]