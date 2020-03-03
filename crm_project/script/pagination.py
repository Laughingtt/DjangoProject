from django.utils.safestring import mark_safe  # 安全传输html标签去前端
from django.http import QueryDict  # request.GET返回的是QueryDict


class Page():
    #SyntaxError: non-default argument follows default argument 非默认参数跟在默认参数后面
    def __init__(self, request, data_count, query_params ,per_pagination=11, per_page=10):
        self.path = request.path_info
        self.page = int(request.GET.get('page', 1))
        self.per_pagination = per_pagination
        self.half = per_pagination // 2
        self.per_page = per_page
        self.data_count = data_count
        self.query_params = query_params
        self.query_params._mutable = True  # _mutable改为True就可以修改字典

    def pre(self):
        return (self.page - 1) * self.per_page

    def next(self):
        return self.page * self.per_page

    @property  # 加入python 内置装饰器，使得方法调用转换为属性调用
    def get_html(self):
        num_page, remainder = divmod(self.data_count, self.per_page)
        if remainder:
            num_page += 1

        pagination = [str(i) for i in range(1, num_page + 1)]  # 页码数据列表

        if self.page > 0 and self.page < self.half + 1:
            start = 1
            end = self.per_pagination
        elif self.page > num_page - self.half:
            start = num_page - self.per_pagination + 1
            end = num_page
        else:
            start = self.page - self.half
            end = self.page + self.half

        #     # 存放li标签的列表
        html_list = []
        # 首页
        self.query_params['page'] = 1
        first_li = '<li><a href="{0}?{1}">首页</a></li>'.format(self.path, self.query_params.urlencode())
        html_list.append(first_li)
        # 上一页
        if self.page == 1:
            prev_li = '<li class="disabled"><a><<</a></li>'
        else:
            self.query_params['page'] = self.page - 1
            prev_li = '<li><a href="{0}?{1}"><<</a></li>'.format(self.path, self.query_params.urlencode())
        html_list.append(prev_li)
        # 中间显示页码数
        for p in pagination[start - 1:end]:
            self.query_params['page'] = p
            page_li = '<li><a href="{0}?{1}">{2}</a></li>'.format(self.path, self.query_params.urlencode(), p)
            html_list.append(page_li)
        # 下一页
        if self.page == num_page:
            next_li = '<li class="disabled"><a>>></a></li>'
        else:
            self.query_params['page'] = self.page + 1
            next_li = '<li><a href="{0}?{1}">>></a></li>'.format(self.path, self.query_params.urlencode())
        html_list.append(next_li)
        # 尾页
        self.query_params['page'] = num_page
        last_li = '<li><a href="{0}?{1}">尾页</a></li>'.format(self.path, self.query_params.urlencode())
        html_list.append(last_li)

        html_str = mark_safe(''.join(html_list))

        return html_str


def page(request):
    # 获取路径
    path = request.path_info
    # print(path,request)
    # 获得当前页码数
    current = request.GET.get('page', 1)
    page = int(current)
    per_pagination = 11  # 显示页码数
    half = per_pagination // 2
    per_page = 10  # 每页显示的数据个数

    # 获取当前页应该对应的页面数据
    pre = (page - 1) * per_page
    next = page * per_page
    print(users[pre:next])
    # 1 0 9
    # 2 10 19
    # 3 20 29
    # 4 30 39
    # 5 40 49

    # 通过当前页来传递页的数字
    num_page, remainder = divmod(len(users), per_page)
    if remainder:
        num_page += 1

    pagination = [str(i) for i in range(1, num_page + 1)]  # 页码数据列表

    if page > 0 and page < 6:
        start = 1
        end = per_pagination
    elif page > 26:
        start = num_page - per_pagination + 1
        end = num_page
    else:
        start = page - half
        end = page + half

    #     # 存放li标签的列表
    html_list = []
    # 首页
    first_li = '<li><a href="{}?page=1">首页</a></li>'.format(path)
    html_list.append(first_li)
    # 上一页
    if page == 1:
        prev_li = '<li class="disabled"><a><<</a></li>'
    else:
        prev_li = '<li><a href="{1}?page={0}"><<</a></li>'.format((page - 1), path)
    html_list.append(prev_li)
    # 中间显示页码数
    for p in pagination[start - 1:end]:
        page_li = '<li><a href="{1}?page={0}">{0}</a></li>'.format(p, path)
        html_list.append(page_li)
    # 下一页
    if page == num_page:
        next_li = '<li class="disabled"><a>>></a></li>'
    else:
        next_li = '<li><a href="{1}?page={0}">>></a></li>'.format((page + 1), path)
    html_list.append(next_li)
    # 尾页
    last_li = '<li><a href="{1}?page={0}">尾页</a></li>'.format(num_page, path)
    html_list.append(last_li)

    html_str = mark_safe(''.join(html_list))
    return render(request, 'crm/page.html',
                  context={"users": users[pre:next], "pagination": pagination[start - 1:end], "html_str": html_str})
