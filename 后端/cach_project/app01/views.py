from django.shortcuts import render, HttpResponse
from app01 import models
import time
import json
from django.core import serializers
from django.views.decorators.cache import cache_page


# Create your views here.
# @cache_page(5)
def cach(request):
    obj = models.User.objects.all()
    # res=json.dumps(list(obj))
    data = serializers.serialize("json", obj)
    return render(request, "cach.html", {"obj": data, "time": time.time()})


def signal(request):
    models.User.objects.create(name="tian", age=19)
    return HttpResponse("添加成功")


from PIL import Image, ImageDraw, ImageFont

import random, os
from django.conf import settings


# 随机生成颜色
def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def png(request):
    # img_path = os.path.join(settings.BASE_DIR, 'static/img/')
    # with open(img_path + '1.png', 'wb') as f:
    #     # 创建image对象并调整大小和颜色
    #     img_obj = Image.new('RGB', (250, 35), random_color())
    #
    #     # 在该图片对象上生成一个画笔对象
    #     draw_obj = ImageDraw.Draw(img_obj)
    #
    #     # 将字体导入并设置字体大小
    #     font_obj = ImageFont.truetype('static/font/kumo.ttf', 28)
    #
    #     temp = []
    #     for i in range(5):
    #         l = chr(random.randint(97, 122))  # 小写字母 chr()返回值是当前整数对应的 ASCII 字符。
    #         b = chr(random.randint(65, 90))  # 大写字母
    #         n = str(random.randint(0, 9))
    #
    #         t = random.choice([l, b, n])
    #         temp.append(t)
    #
    #         draw_obj.text((i * 40 + 35, 0), t, fill=random_color(), font=font_obj)
    #
    #     img_obj.save(f)
    # with open('1.png', 'rb') as f:
    #     image_data = f.read()

    # 创建image对象并调整大小和颜色
    img_obj = Image.new('RGB', (250, 35), random_color())

    # 在该图片对象上生成一个画笔对象
    draw_obj = ImageDraw.Draw(img_obj)

    # 将字体导入并设置字体大小
    font_obj = ImageFont.truetype('static/font/kumo.ttf', 28)

    temp = []
    for i in range(5):
        l = chr(random.randint(97, 122))  # 小写字母 chr()返回值是当前整数对应的 ASCII 字符。
        b = chr(random.randint(65, 90))  # 大写字母
        n = str(random.randint(0, 9))

        t = random.choice([l, b, n])
        temp.append(t)

        draw_obj.text((i * 40 + 35, 0), t, fill=random_color(), font=font_obj)

    from io import BytesIO
    f1 = BytesIO()
    img_obj.save(f1, format="PNG")
    image_data = f1.getvalue()

    return HttpResponse(image_data, content_type="image/png")
