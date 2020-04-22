# -*- coding: UTF-8 -*-
""""=================================================
@Project -> File   ：Django -> 二叉树之有序列表
@IDE    ：PyCharm
@Author ：爱跳水的温文尔雅的laughing
@Date   ：2020/4/2 21:56
@Desc   ：
=================================================="""
from rest_framework import serializers
from .models import Book


class PublisherSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=32)


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=32)


# serializers.py 文件
# class BookSerializer(serializers.Serializer):
#     id = serializers.IntegerField(required=False)
#     title = serializers.CharField(max_length=32)
#     pub_time = serializers.DateField()
#     category = serializers.CharField(source="get_category_display", read_only=True)
#     post_category = serializers.IntegerField(write_only=True)
#
#     publisher = PublisherSerializer(read_only=True)
#     # 内部通过外键关系的id找到了publisher_obj
#     authors = AuthorSerializer(many=True, read_only=True)
#     publisher_id = serializers.IntegerField(write_only=True)
#     author_list = serializers.ListField(write_only=True)
#
#     def create(self, validated_data):
#         # validated_data 校验通过的数据 就是book_obj
#         # 通过ORM操作给Book表增加数据
#         print(validated_data)
#         book_obj = Book.objects.create(title=validated_data["title"], pub_time=validated_data["pub_time"],
#                                        category=validated_data["post_category"],
#                                        publisher_id=validated_data["publisher_id"])
#         print(book_obj)
#         book_obj.authors.add(*validated_data["author_list"])
#         return book_obj

class BookSerializer(serializers.ModelSerializer):
    """
    读和写不一致的情况下，重新读，重新定义读出来的值的方法为SerializerMethodField，
    """
    category_display = serializers.SerializerMethodField(read_only=True)
    publisher_info = serializers.SerializerMethodField(read_only=True)
    authors_info = serializers.SerializerMethodField(read_only=True)

    # get+字段名,为钩子函数，返回值为定义的字段的值,obj为Book_obj对象
    def get_category_display(self, obj):
        # obj 就是序列化的每个Book对象
        return obj.get_category_display()

    def get_authors_info(self, obj):
        authors_querset = obj.authors.all()
        return [{"id": author.id, "name": author.name} for author in authors_querset]

    def get_publisher_info(self, obj):
        publisher_obj = obj.publisher
        return {"id": publisher_obj.id, "title": publisher_obj.title}

    def validate_title(self, value):
        if "python" not in value.lower():
            raise serializers.ValidationError("标题必须含有Python")
        return value

    class Meta:
        model = Book
        fields = "__all__"
        # exclude=["id"]
        # 会让你这些所有的外键关系变成read_only = True
        # depth = 1
        # 将原本的字段设置为只写模式，所以只能写入对应的id
        extra_kwargs = {"publisher": {"write_only": True}, "authors": {"write_only": True},
                        "category": {"write_only": True}}
