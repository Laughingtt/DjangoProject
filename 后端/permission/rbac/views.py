from django.shortcuts import render, redirect, reverse
from rbac import models
from django.conf import settings
from rbac import models
from rbac.forms import RoleForm, MenuForm, PermissionForm


def session_func(request, user):
    """
    将获得的url权限和菜单权限都加入到session中
    """
    # 1. 查当前登录用户拥有的权限
    permission_query = user.roles.filter(permissions__url__isnull=False).values(
        'permissions__url',
        'permissions__title',
        'permissions__id',
        'permissions__name',
        'permissions__parent_id',
        'permissions__parent__name',
        'permissions__menu_id',
        'permissions__menu__title',
        'permissions__menu__icon',
        'permissions__menu__weight',
    ).distinct()

    # 存放权限信息
    permission_dict = {}

    # 存放菜单信息

    menu_dict = {}

    for item in permission_query:
        permission_dict[item['permissions__name']] = {'url': item['permissions__url'],
                                                      'id': item['permissions__id'],
                                                      'pid': item['permissions__parent_id'],
                                                      'pname': item['permissions__parent__name'],
                                                      'title': item['permissions__title']}

        menu_id = item.get('permissions__menu_id')

        if not menu_id:
            continue

        if menu_id not in menu_dict:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'weight': item['permissions__menu__weight'],
                'children': [
                    {'title': item['permissions__title'], 'url': item['permissions__url'],
                     'id': item['permissions__id'], 'pid': item['permissions__parent_id']}
                ]
            }
        else:
            menu_dict[menu_id]['children'].append(
                {'title': item['permissions__title'], 'url': item['permissions__url'], 'id': item['permissions__id'],
                 'pid': item['permissions__parent_id']})

    # # 2. 将权限信息写入到session
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict

    # 将菜单信息写入到session
    request.session[settings.MENU_SESSION_KEY] = menu_dict


def login(request):
    """
    登录后获取用户的角色的相关权限并加入到session中
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        user = models.User.objects.filter(name=username, password=password).first()
        # print("111",user)
        session_func(request, user)

        return redirect(reverse('web:customer'))
    else:
        err_msg = '用户名或密码错误'
        return render(request, 'login.html', {'err_msg': err_msg})

    return render(request, 'login.html')


"""角色管理"""


def role_list(request):
    all_roles = models.Role.objects.all()
    roles = models.Menu.objects.all().values("id", "title", "permission__title")
    for i in roles:
        print(i)
    form_obj = RoleForm()
    return render(request, "rbac/role_list.html", context={"all_roles": all_roles, "form_obj": form_obj})


def role_edit(request, edit_id=None):
    obj = models.Role.objects.filter(id=edit_id).first()
    form_obj = RoleForm(instance=obj)
    if request.method == "POST":
        form_obj = RoleForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:role_list'))
    return render(request, 'rbac/role_edit.html', {"form_obj": form_obj})


def role_del(request, del_id):
    models.Role.objects.filter(id=del_id).delete()
    return redirect(reverse('rbac:role_list'))


"""菜单管理"""


def menu_list(request):
    all_menus = models.Menu.objects.all()
    all_permission = models.Permission.objects.all().values('id', 'title', 'url', 'name', 'parent_id', 'menu_id',
                                                            'menu__title')
    return render(request, "rbac/menu_list.html", context={"all_menus": all_menus, "all_permission": all_permission})


def menu_add(request, edit_id=None):
    obj = models.Menu.objects.filter(id=edit_id).first()
    form_obj = MenuForm(instance=obj)
    if request.method == "POST":
        form_obj = MenuForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'rbac/menu_add.html', {"form_obj": form_obj})


def menu_del(request, del_id):
    models.Menu.objects.filter(id=del_id).delete()
    return redirect(reverse('rbac:menu_list'))


"""权限管理"""


def permission_add(request, edit_id=None):
    obj = models.Permission.objects.filter(id=edit_id).first()
    form_obj = PermissionForm(instance=obj)
    if request.method == "POST":
        form_obj = PermissionForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'rbac/permission_add.html', {"form_obj": form_obj})


def permission_del(request, del_id):
    models.Permission.objects.filter(id=del_id).delete()
    return redirect(reverse('rbac:menu_list'))
