# -*- coding: utf-8 -*-
# __author__ = "maple"
from rest_framework.throttling import SimpleRateThrottle
import time
VISIT_RECORD = {}

class MyThrottle(object):
    """
    一分钟允许访问5次
    """
    def __init__(self):
        self.history = []

    def allow_request(self, request, view):
        # 获取用户的IP地址
        ip = request.META.get("REMOTE_ADDR", "")
        # self.key = self.get_cache_key()
        # self.cache.get(self.key, [])
        if ip not in VISIT_RECORD:
            VISIT_RECORD[ip] = [time.time(),]
        else:
            history = VISIT_RECORD[ip]
            self.history = history
            history.insert(0, time.time())
            # 确保列表时间是允许范围之内
            while self.history[0] - self.history[-1] > 60:
                self.history.pop()
            # 判断列表长度
            if not len(self.history) <= 5:
                return False
        return True

    # 等待时间
    # [最近时间，      最老时间]
    def wait(self):
        return 60-(self.history[0] - self.history[-1])


class DRFThrottle(SimpleRateThrottle):
    scope = "WD"
    def get_cache_key(self, request, view):
        # 拿IP地址
        return self.get_ident(request)