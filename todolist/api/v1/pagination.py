from rest_framework.pagination import PageNumberPagination

class TodoListPagination(PageNumberPagination):
    page_query_param = "pagenum"
    page_size_query_param = "size"
    max_page_size = 10
