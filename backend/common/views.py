from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated


class CommonView(APIView):
    permission_classes = [IsAuthenticated,]
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    serializer_class = None

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def paginated_response(self, queryset, request):
        queryset = self.filter_queryset(queryset)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if self.serializer_class:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return paginator.get_paginated_response(page)