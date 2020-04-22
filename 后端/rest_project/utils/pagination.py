from rest_framework import pagination


class MyPaginator(pagination.PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 3


class LimitOffsetPaginator(pagination.LimitOffsetPagination):
    default_limit = 1
    limit_query_param = 'limit'
    offset_query_param = 'offset'


class CursorPaginator(pagination.CursorPagination):
    cursor_query_param = 'cursor'
    ordering = 'id'
    page_size = 1
