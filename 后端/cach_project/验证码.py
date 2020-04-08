import random


def v_code():
    lis = []
    for i in range(5):
        l = chr(random.randint(97, 122))  # 小写字母 chr()返回值是当前整数对应的 ASCII 字符。
        b = chr(random.randint(65, 90))  # 大写字母
        n = str(random.randint(0, 9))
        t = random.choice([l, b, n])
        lis.append(t)
    print(''.join(lis))


from PIL import Image, ImageDraw, ImageFont

# 随机生成颜色
def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def code():
    with open('1.png', 'wb') as f:
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

        img_obj.save(f)


code()
