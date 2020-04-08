from django.conf.urls import url, include
from django.contrib import admin
from rbac import views

urlpatterns = [
    url(r'^role_list/', views.role_list, name="role_list"),
    url(r'^role_add/', views.role_edit, name="role_add"),
    url(r'^role_edit/(?P<edit_id>\d+)/$', views.role_edit, name="role_edit"),
    url(r'^role_del/(?P<del_id>\d+)/$', views.role_del, name="role_del"),

    # 菜单
    url(r'^menu_list/', views.menu_list, name="menu_list"),
    url(r'^menu_add/', views.menu_add, name="menu_add"),
    url(r'^menu_edit/(?P<edit_id>\d+)/$', views.menu_add, name="menu_edit"),
    url(r'^menu_del/(?P<del_id>\d+)/$', views.menu_del, name="menu_del"),

    # 权限
    url(r'^menu_list/', views.menu_list, name="permission_list"),
    url(r'^permission_add/', views.permission_add, name="permission_add"),
    url(r'^permission_edit/(?P<edit_id>\d+)/$', views.permission_add, name="permission_edit"),
    url(r'^permission_del/(?P<del_id>\d+)/$', views.permission_del, name="permission_del"),

]
