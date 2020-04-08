from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import HttpResponse
import re


class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 对权限进行校验
        # 1. 当前访问的URL
        current_url = request.path_info
        
        # 白名单的判断
        for i in settings.WHITE_URL_LIST:
            if re.match(i, current_url):
                return
        
        # 2. 获取当前用户的所有权限信息
        
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        
        request.breadcrumb_list = [
            {"title": '首页', 'url': '#'},
        ]
        
        # 3. 权限的校验
        print(permission_dict)
        for item in permission_dict.values():
            url = item['url']
            if re.match("^{}$".format(url), current_url):
                pid = item['pid']
                id = item['id']
                pname = item['pname']
                if pid:
                    # 表示当前权限是子权限，让父权限是展开
                    request.current_menu_id = pid
                    request.breadcrumb_list.extend(
                        [{"title": permission_dict[pname]['title'], 'url': permission_dict[pname]['url']},
                         {"title": item['title'], 'url': item['url']}]
                    )
                
                else:
                    # 表示当前权限是父权限，要展开的二级菜单
                    request.current_menu_id = id
                    # 添加面包屑导航
                    request.breadcrumb_list.append({"title": item['title'], 'url': item['url']})
                
                return
        
        else:
            return HttpResponse('没有权限')
