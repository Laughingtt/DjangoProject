import json
data = {
    1: {'url': '/customer/list/', 'id': 1, 'pid': None, 'title': '客户列表'},
    2: {'url': '/customer/add/', 'id': 2, 'pid': 1, 'title': '添加客户'},
    3: {'url': '/customer/edit/(?P<cid>\\d+)/', 'id': 3, 'pid': 1, 'title': '编辑客户'},
    4: {'url': '/customer/del/(?P<cid>\\d+)/', 'id': 4, 'pid': 1, 'title': '删除客户'},
    5: {'url': '/payment/list/', 'id': 5, 'pid': None, 'title': '缴费列表'},
    6: {'url': '/payment/add/', 'id': 6, 'pid': 5, 'title': '添加缴费记录'},
    7: {'url': '/payment/edit/(?P<pid>\\d+)/', 'id': 7, 'pid': 5, 'title': '编辑缴费记录'},
    8: {'url': '/payment/del/(?P<pid>\\d+)/', 'id': 8, 'pid': 5, 'title': '删除缴费记录'}}

# data2 = {'1': {'url': '/customer/list/', 'id': 1, 'pid': None, 'title': '客户列表'},
#          '2': {'url': '/customer/add/', 'id': 2, 'pid': 1, 'title': '添加客户'},
#          '3': {'url': '/customer/edit/(?P<cid>\\d+)/', 'id': 3, 'pid': 1, 'title': '编辑客户'},
#          '4': {'url': '/customer/del/(?P<cid>\\d+)/', 'id': 4, 'pid': 1, 'title': '删除客户'},
#          '5': {'url': '/payment/list/', 'id': 5, 'pid': None, 'title': '缴费列表'},
#          '6': {'url': '/payment/add/', 'id': 6, 'pid': 5, 'title': '添加缴费记录'},
#          '7': {'url': '/payment/edit/(?P<pid>\\d+)/', 'id': 7, 'pid': 5, 'title': '编辑缴费记录'},
#          '8': {'url': '/payment/del/(?P<pid>\\d+)/', 'id': 8, 'pid': 5, 'title': '删除缴费记录'}}


ret = json.dumps(data)

print(json.loads(ret))

