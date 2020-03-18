from django import template

register = template.Library()

from django.conf import settings
import re
from collections import OrderedDict


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    
    order_dict = OrderedDict()
    
    for key in sorted(menu_dict, key=lambda x: menu_dict[x]['weight'], reverse=True):
        order_dict[key] = menu_dict[key]
        
        item = order_dict[key]
        
        item['class'] = 'hide'
        
        for i in item['children']:
            
            if i['id'] == request.current_menu_id:
                i['class'] = 'active'
                item['class'] = ''
    
    return {"menu_list": order_dict}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    return {'breadcrumb_list': request.breadcrumb_list}


@register.filter
def has_permission(request, permission):
    if permission in request.session.get(settings.PERMISSION_SESSION_KEY):
        return True


@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()
    params._mutable = True
    params['rid'] = rid
    return params.urlencode()
