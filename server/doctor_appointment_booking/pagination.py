from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class NeatPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        current_page = self.page.number
        paginator = self.page.paginator

        return Response({
            'pagination': {
                'current_page': current_page,
                'count': paginator.count,
                'pages': paginator.num_pages,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'has_previous': self.page.has_previous(),
                'has_next': self.page.has_next()
            },
            'results': data
        })
