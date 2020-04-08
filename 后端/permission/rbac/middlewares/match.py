import re

a = re.search("/login/", "/login/11")
print(a)

2.
应用rbac组件
1.
拷贝rbac组件
到
新的项目中
并注册APP

2.
配置权限的相关信息
#  ###### 权限相关的配置 ######
PERMISSION_SESSION_KEY = 'permissions'
MENU_SESSION_KEY = 'menus'
WHITE_URL_LIST = [
    r'^/login/$',
    r'^/logout/$',
    r'^/reg/$',
    r'^/admin/.*',
]

3.
创建跟权限相关的表（删除之前的迁移文件的记录）
执行命令：
python
manage.py
makemigrations
python
manage.py
migrate

4.
录入权限信息
创建超级用户
录入所有权限信息
创建角色
给角色分权限
创建用户
给用户分角色

5.
在登录成功之后
写入权限和菜单的信息
到session中

6.
配置上中间件
进行权限的校验

7.
使用动态的菜单
导入静态文件
< link
rel = "stylesheet"
href = "{% static 'css/menu.css' %}" >

使用inclusion_tag
< div


class ="left-menu" >

< div


class ="menu-body" >


{ % load
rbac %}
{ % menu
request %}
< / div >
< / div >
