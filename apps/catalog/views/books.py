from rest_framework import status, generics
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from apps.catalog import serializers
from apps.catalog.models import Book, Genre

class BooksListView(ModelViewSet):
    permission_classes=[AllowAny,]
    serializer_class=serializers.BookListSerializer
    queryset=Book.objects.all()
    filterset_fields={
        'genre':['exact'],
        'author':['exact'],
        'published_date':['year', 'month', 'month__in', 'year__in',
                 'month__gte', 'month__lte','year__gte','year__lte','gte','lte'],
    }

    @extend_schema(
        responses={200: serializer_class},
        methods=['GET'],
        tags=['Book Overview']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class GenreList(generics.ListAPIView):
    queryset=Genre.objects.all()
    serializer_class=serializers.GenreSerializer

    @extend_schema(
        responses={200: serializer_class},
        methods=['GET'],
        tags=['Book Overview']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)