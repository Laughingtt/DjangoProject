from django.conf import settings


def init_permission(request, user):
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
