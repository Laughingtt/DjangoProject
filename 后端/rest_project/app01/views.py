from django.shortcuts import render, HttpResponse
from django.views import View
from . import models
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer
from rest_framework import viewsets
from .models import User
import uuid
from .auth import MyAuth


# Create your views here.
#
# class RestTest(APIView):
#     def get(self, request):
#         book_queryset = models.Book.objects.all()
#         ser_obj = BookSerializer(book_queryset, many=True)
#         return Response(ser_obj.data)
#
#     def post(self, request):
#         print(request.data)  # 接收到的数据
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():  # 验证字符合法性
#             serializer.save()
#             return Response(serializer.validated_data)
#         else:
#             return Response(serializer.errors)
#
#
# class RestPut(APIView):
#     def get(self, request, book_id):
#         book_obj = models.Book.objects.filter(id=book_id).first()
#         ser_obj = BookSerializer(book_obj)
#         return Response(ser_obj.data)
#
#     # request.data为post发送的数据
#     def put(self, request, book_id):
#         book_obj = models.Book.objects.filter(id=book_id).first()
#         ser_obj = BookSerializer(instance=book_obj, data=request.data, partial=True)
#         # partial为局部更新
#         if ser_obj.is_valid():
#             ser_obj.save()
#             return Response(ser_obj.validated_data)  # 验证过的数据
#         return Response(ser_obj.errors)
#
#     def delete(self, request, book_id):
#         book_obj = models.Book.objects.filter(id=book_id).first()
#         if not book_obj:
#             return Response("你需要删除的对象不存在")
#         book_obj.delete()
#         return Response("成功删除")
#
#
# class BookModelView(viewsets.ModelViewSet):
#     queryset = models.Book.objects.all()
#     serializer_class = BookSerializer


class AuthTest(APIView):
    """登录认证后发送给前端token串"""

    def post(self, request):
        name = request.data.get("name", "")
        pwd = request.data.get("pwd", "")
        # 校验用户名和密码是否正确
        user_obj = User.objects.filter(name=name, pwd=pwd).first()
        if user_obj:
            user_obj.token = uuid.uuid4()
            user_obj.save()
            return Response(user_obj.token)
        else:
            return Response("用户名或密码错误")


class TestView(APIView):
    # 认证token合法性
    authentication_classes = [MyAuth, ]

    def get(self, request):
        return Response("测试认证组件")


from utils.pagination import MyPaginator, LimitOffsetPaginator, CursorPaginator
from .throttle import MyThrottle,DRFThrottle
from .permission import MyPermission

class BookModelView(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer
    # authentication_classes = [MyAuth, ]
    # permission_classes = [MyPermission, ] #认证
    # pagination_class = MyPaginator
    # pagination_class = LimitOffsetPaginator
    pagination_class = CursorPaginator
    throttle_classes = [DRFThrottle, ]
