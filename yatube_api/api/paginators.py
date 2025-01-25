from rest_framework.pagination import LimitOffsetPagination

class PostPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

    def paginate_queryset(self, queryset, request, view=None):
        # Если параметры `limit` и `offset` отсутствуют, отключаем пагинацию
        if 'limit' not in request.query_params and 'offset' not in request.query_params:
            return None
        return super().paginate_queryset(queryset, request, view)
