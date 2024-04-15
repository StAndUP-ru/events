from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    '''
    Пользовательская пагинация для представлений.
    '''
    page_size = 6
    page_size_query_param = 'page_size'

class CustomUserPagination(PageNumberPagination):
    '''
    Пользовательская пагинация для представлений.
    '''
    page_size = 20
