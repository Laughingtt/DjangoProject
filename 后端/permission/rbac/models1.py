from django.db import models


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(max_length=32, verbose_name='标题')
    url = models.CharField(max_length=32, verbose_name='权限')

    is_menu = models.BooleanField(default=False, verbose_name='是否是菜单')
    icon = models.CharField(max_length=32, verbose_name='图标', null=True, blank=True)

    class Meta:
        verbose_name_plural = '权限表' #admin页面中显示的复数形式的名字，最外层的名字
        verbose_name = '权限表'   #下一层的名字

    def __str__(self):
        return self.title


class Role(models.Model):
    name = models.CharField(max_length=32, verbose_name='角色名称')
    permissions = models.ManyToManyField(to='Permission', verbose_name='角色所拥有的权限', blank=True)

    def __str__(self):
        return self.name


class User(models.Model):
    """
    用户表
    """
    name = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    roles = models.ManyToManyField(to='Role', verbose_name='用户所拥有的角色', blank=True)

    def __str__(self):
        return self.name
