from rest_framework.pagination import (
    PageNumberPagination as _PageNumberPagination,
    LimitOffsetPagination
)
from collections import OrderedDict
from rest_framework.response import Response


class PageNumberPagination(_PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 50
    max_page_size = 10000

    def get_paginated_response(self, data):
        code = 200
        msg = 'success'
        if not data:
            code = 200
            msg = "Data Not Found"

        return Response(OrderedDict([
            ('code', code),
            ('msg', msg),
            ('page_size', self.get_page_size(self.request)),
            ('count', self.page.paginator.count),
            ('data', data),
        ]))