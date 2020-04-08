import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_homework.settings")
import django

django.setup()

from app01 import models

ret = models.Book.objects.all()

# 查找所有书名里包含金老板的书
ret = models.Book.objects.filter(title__contains='金')
# 查找出版日期是2018年的书
ret = models.Book.objects.filter(publish_date__year='2018').values()
# 查找出版日期是2017年的书名
ret = models.Book.objects.filter(publish_date__year='2017').values()
# 查找价格大于10元的书
ret = models.Book.objects.filter(price__gt='10').values('price')
# 查找价格大于10元的书名和价格
ret = models.Book.objects.filter(price__gt='10').values('title','price')
# 查找memo字段是空的书
ret = models.Book.objects.filter(memo__isnull=True)
# 查找在北京的出版社
ret = models.Publisher.objects.filter(city='北京')
# 查找名字以沙河开头的出版社startswith
ret = models.Publisher.objects.filter(name__startswith='沙河')
# 查找“沙河出版社”出版的所有书籍
ret = models.Book.objects.filter(publisher__name='沙河出版社')
ret = models.Publisher.objects.filter(name='沙河出版社').values('book__title')
# 查找每个出版社出版价格最高的书籍价格
from django.db.models import *
ret = models.Publisher.objects.annotate(Max('book__price')).values()
# 查找每个出版社的名字以及出的书籍数量
ret = models.Publisher.objects.annotate(count=Count('book__id')).values('name','count')
#
# 查找作者名字里面带“小”字的作者
ret = models.Author.objects.filter(name__contains='小')
# 查找年龄大于30岁的作者
ret = models.Author.objects.filter(age__gt='30')
# 查找手机号是155开头的作者
ret = models.Author.objects.filter(phone__startswith='155')
# 查找手机号是155开头的作者的姓名和年龄
ret = models.Author.objects.filter(phone__startswith='155').values('name','age')
# 查找每个作者写的价格最高的书籍价格
ret = models.Author.objects.annotate(max=Max('book__price')).values('name','max')
# 查找每个作者的姓名以及出的书籍数量
ret = models.Author.objects.annotate(count=Count('book__id')).values('name','count')
#
# 查找书名是“跟金老板学开车”的书的出版社
ret = models.Publisher.objects.filter(book__title='跟金老板学开车')
# 查找书名是“跟金老板学开车”的书的出版社所在的城市
ret = models.Publisher.objects.filter(book__title='跟金老板学开车').values('book__title','city')
# 查找书名是“跟金老板学开车”的书的出版社的名称
ret = models.Publisher.objects.filter(book__title='跟金老板学开车').values('name')
# 查找书名是“跟金老板学开车”的书的出版社出版的其他书籍的名字和价格
r = models.Publisher.objects.filter(book__title='跟金老板学开车').first()
res = models.Book.objects.filter(publisher=r).exclude(title='跟金老板学开车')
print(res)
#
# 查找书名是“跟金老板学开车”的书的所有作者
ret = models.Author.objects.filter(book__title='跟金老板学开车').values('name')
# 查找书名是“跟金老板学开车”的书的作者的年龄
ret = models.Author.objects.filter(book__title='跟金老板学开车').values('name','age')
# 查找书名是“跟金老板学开车”的书的作者的手机号码
ret = models.Author.objects.filter(book__title='跟金老板学开车').values('name','age','phone')
# 查找书名是“跟金老板学开车”的书的作者们的姓名以及出版的所有书籍名称和价钱
ret = models.Author.objects.filter(book__title='跟金老板学开车').values('name','book__title','book__price')


print(ret)
print(ret.query)
