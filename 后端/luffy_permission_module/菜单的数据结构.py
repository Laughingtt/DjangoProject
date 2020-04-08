data = [
    {
        'permissions__url': '/customer/list/',
        'permissions__title': '客户列表',
        'permissions__menu_id': 1,
        'permissions__menu__title': '信息管理',
        'permissions__menu__icon': 'fa-clipboard'
    }, {
        'permissions__url': '/customer/add/',
        'permissions__title': '添加客户',
        'permissions__menu_id': None,
        'permissions__menu__title': None,
        'permissions__menu__icon': None
    }, {
        'permissions__url': '/customer/edit/(?P<cid>\\d+)/',
        'permissions__title': '编辑客户',
        'permissions__menu_id': None,
        'permissions__menu__title': None,
        'permissions__menu__icon': None
    },
    {
        'permissions__url': '/payment/list/',
        'permissions__title': '缴费列表',
        'permissions__menu_id': 1,
        'permissions__menu__title': '信息管理',
        'permissions__menu__icon': 'fa-clipboard'
    },
]

menu_dict = {}

for item in data:
    
    menu_id = item.get('permissions__menu_id')
    
    if not menu_id:
        continue
    
    if menu_id not in menu_dict:
        menu_dict[menu_id] = {
            'title': item['permissions__menu__title'],
            'icon': item['permissions__menu__icon'],
            'children': [
                {'title': item['permissions__title'], 'url': item['permissions__url']}
            ]
        }
    else:
        menu_dict[menu_id]['children'].append({'title': item['permissions__title'], 'url': item['permissions__url']})

# print(menu_dict)

"""

{
    1 : {
        'title' : '信息管理',
        'icon'  : 'fa-clipboard',
        'children': [
            {'title':'客户列表','url':'/customer/list/'}
        ]
    },
    2 : {
        'title' : '财务管理',
        'icon'  : 'fa-clipboard',
        'children': [
            {'title':'客户列表','url':'/customer/list/'}
        ]
    }
}

"""
print({
    "1": {
        'title': '信息管理',
        'icon': 'fa-clipboard',
        'children': [
            {'title': '客户列表', 'url': '/customer/list/'}
        ]
    },
    "2": {
        'title': '财务管理',
        'icon': 'fa-clipboard',
        'children': [
            {'title': '客户列表', 'url': '/customer/list/'}
        ]
    }
})
