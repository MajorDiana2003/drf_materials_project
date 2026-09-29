from rest_framework.pagination import PageNumberPagination

class MaterialPagination(PageNumberPagination):
    page_size = 5  # Количество элементов по умолчанию на одной странице
    page_size_query_param = 'page_size'  # Позволяет клиенту задавать свой размер страницы через ?page_size=
    max_page_size = 50  # Максимально допустимый размер страницы
