# api/pagination.py

from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Allow the client to set a custom page size via query param
    max_page_size = 100  # Maximum page size allowed
