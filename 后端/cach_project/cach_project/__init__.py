from django.core.signals import request_finished  # 请求结束后，自动触发
from django.core.signals import request_started  # 请求到来前，自动触发
from django.core.signals import got_request_exception  # 请求异常后，自动触发

from django.db.models.signals import class_prepared # 程序启动时，检测已注册的app中modal类，对于每一个类，自动触发
from django.db.models.signals import pre_init, post_init  # django的model执行其构造方法前，自动触发
from django.db.models.signals import pre_save, post_save # django的model对象保存前，自动触发
from django.db.models.signals import pre_delete, post_delete    # django的model对象删除前，自动触发
from django.db.models.signals import m2m_changed
from django.db.models.signals import pre_migrate, post_migrate

from django.test.signals import setting_changed   # 使用test测试修改配置文件时，自动触发
from django.test.signals import template_rendered   # 使用test测试渲染模板时，自动触发

from django.db.backends.signals import connection_created


def callback(sender, **kwargs):
    print("xxoo_callback")
    print(sender, kwargs)


post_save.connect(callback)
# xxoo指上述导入的内容