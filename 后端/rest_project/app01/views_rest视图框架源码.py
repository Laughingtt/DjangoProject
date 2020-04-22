from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from djangoDemo.models import Book
from .serializers import BookSerializer
from rest_framework.viewsets import ViewSetMixin


from rest_framework import views  # APIView
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins



# Create your views here.
# queryset不同
# 序列化器不同
# def get():
# def post():

class GenericAPIView(APIView):
    queryset = None
    serializer_class = None
    
    def get_queryset(self):
        return self.queryset.all()
    
    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)


class ListModelMixin(object):
    def list(self, request):
        queryset = self.get_queryset()
        ser_obj = self.get_serializer(queryset, many=True)
        return Response(ser_obj.data)
    

class CreateModelMixin(object):
    def create(self, request):
        ser_obj = self.get_serializer(data=request.data)
        if ser_obj.is_valid():
            ser_obj.save()
            return Response(ser_obj.validated_data)
        return Response(ser_obj.errors)
    

class RetrieveModelMixin(object):
    def retrieve(self, request, id):
        book_obj = self.get_queryset().filter(id=id).first()
        ser_obj = BookSerializer(book_obj)
        return Response(ser_obj.data)
    

class UpdateModelMixin(object):
    def update(self, request, id):
        book_obj = self.get_queryset().filter(id=id).first()
        ser_obj = self.get_serializer(instance=book_obj, data=request.data, partial=True)
        if ser_obj.is_valid():
            ser_obj.save()
            return Response(ser_obj.validated_data)
        return Response(ser_obj.errors)
    
    
class DestroyModelMixin(object):
    def destroy(self, request, id):
        book_obj = self.get_queryset().filter(id=id).first()
        if not book_obj:
            return Response("删除的对象不存在")
        book_obj.delete()
        return Response("")
    

class ListCreateAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    pass

    
class RetrieveUpdateDestroyAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    pass


class ModelViewSet(ViewSetMixin, ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    pass
 
    
class BookView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    
    # def get(self, request):
    #     # 调用外部的get方法
    #     # book_queryset = Book.objects.all()
    #     queryset = self.get_queryset()
    #     # queryset = self.queryset.all()
    #     # [book_obj, ]
    #     # 用序列化器进行序列化
    #     # ser_obj = BookSerializer(book_queryset, many=True)
    #     ser_obj = self.get_serializer(queryset, many=True)
    #     return Response(ser_obj.data)
    
    def get(self, request):
        return self.list(request)

    # def post(self, request):
    #     # 确定数据类型以及数据结构
    #     # 对妹子传过来的数据进行校验
    #     # book_obj = request.data
    #     # print(book_obj)
    #     # ser_obj = BookSerializer(data=book_obj)
    #     ser_obj = self.get_serializer(data=request.data)
    #     if ser_obj.is_valid():
    #         ser_obj.save()
    #         return Response(ser_obj.validated_data)
    #     return Response(ser_obj.errors)
    def post(self, request):
        return self.create(request)
    
    
class BookEditView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get(self, request, id):
        # book_obj = Book.objects.filter(id=id).first()
        # ser_obj = BookSerializer(book_obj)
        # return Response(ser_obj.data)
        return self.retrieve(request, id)
    
    def put(self, request, id):
        # book_obj = Book.objects.filter(id=id).first()
        # ser_obj = BookSerializer(instance=book_obj, data=request.data, partial=True)
        # if ser_obj.is_valid():
        #     ser_obj.save()
        #     return Response(ser_obj.validated_data)
        # return Response(ser_obj.errors)
        return self.update(request, id)

    def delete(self, request, id):
        # book_obj = Book.objects.filter(id=id).first()
        # if not book_obj:
        #     return Response("删除的对象不存在")
        # book_obj.delete()
        # return Response("")
        return self.destroy(request, id)
    

class BookModelView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    









