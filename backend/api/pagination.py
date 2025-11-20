"""Custom pagination for the API."""
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination for the API."""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500
