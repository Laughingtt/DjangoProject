# -*- coding: utf-8 -*-
# __author__ = "maple"


class MyPermission(object):
    message = "权限不足"
    def has_permission(self, request, view):
        # 权限逻辑
        # 认证已经执行完了
        user_obj = request.user
        if user_obj.type == 1:
            return False
        else:
            return True