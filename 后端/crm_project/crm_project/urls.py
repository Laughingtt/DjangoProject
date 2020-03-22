"""crm_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from crm import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login, name='login'),
    url(r'^v_code/', views.v_code, name='v_code'),
    url(r'^register/', views.register, name='register'),
    # url(r'^index/', views.index, name='index'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^change_pwd/', views.change_pwd, name='change_pwd'),
    url(r'^crm/', include('crm.urls')),
    url(r'^rbac/', include('rbac.urls', namespace="rbac")),

]
