# from django import template
#
# register = template.Library()
#
# from django.conf import settings
# import re
#
# @register.inclusion_tag('rbac/menu.html')
# def menu(request):
#     menu_list = request.session.get(settings.MENU_SESSION_KEY)
#     print(menu_list)
#     # for item in menu_list:
#     #     url = item['url']
#     #     if re.match('^{}$'.format(url), request.path_info):
#     #         item['class'] = 'active'
#     #         break
#
#     return {"menu_list": menu_list} #将参数传递给menu.html


from django import template

register = template.Library()

from django.conf import settings
import re
from collections import OrderedDict


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    menu_list = request.session.get(settings.MENU_SESSION_KEY)

    order_dict = OrderedDict()

    # for i in sorted(menu_list, key=lambda x: menu_list[x]['weight'],reverse=True):
    #     order_dict[i] = menu_list[i]
    #
    # for item in order_dict.values():
    #     item['class'] = 'hide'
    #
    #     for i in item['children']:
    #
    #         if re.match("^{}$".format(i['url']), request.path_info):
    #             i['class'] = 'active'
    #             item['class'] = ''

    for key in sorted(menu_list, key=lambda x: menu_list[x]['weight'], reverse=True):
        order_dict[key] = menu_list[key]

        item = order_dict[key]

        item['class'] = 'hide'

        for i in item['children']:

            if re.match("^{}$".format(i['url']), request.path_info):
                i['class'] = 'active'
                item['class'] = ''

    return {"menu_list": order_dict}


# @register.inclusion_tag('rbac/bread.html')
# def bread(request):
#     return request

@register.inclusion_tag('rbac/bread.html')
def breadcrumb(request):
    return {'breadcrumb_list': request.breadcrumb_list}


@register.filter
def has_permission(request, permission):
    if permission in request.session.get(settings.PERMISSION_SESSION_KEY):
        return True
