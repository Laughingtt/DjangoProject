from django.db import models


class Menu(models.Model):
    """
    一级菜单
    """
    title = models.CharField(max_length=32, unique=True,verbose_name='标题')
    icon = models.CharField(max_length=32, verbose_name='图标', null=True, blank=True)
    weight = models.IntegerField(default=1,verbose_name='权重')
    
    class Meta:
        verbose_name_plural = '菜单表'
        verbose_name = '菜单表'
    
    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    有关联Menu的是二级菜单
    没有关联Menu的不是二级菜单，是不可以做菜单的权限
    
    
    """
    title = models.CharField(max_length=32, verbose_name='标题')
    url = models.CharField(max_length=32, verbose_name='权限')
    menu = models.ForeignKey('Menu', null=True, blank=True,verbose_name='菜单')
    
    parent = models.ForeignKey('Permission', null=True, blank=True,verbose_name='父权限')
    name = models.CharField(max_length=32, null=True, blank=True, unique=True,verbose_name='URL别名')
    
    class Meta:
        verbose_name_plural = '权限表'
        verbose_name = '权限表'
    
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
