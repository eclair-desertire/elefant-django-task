from rest_framework import status, generics
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from apps.catalog import serializers
from apps.catalog.models import Book, Genre
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class BooksListView(ModelViewSet):
    permission_classes=[AllowAny,]
    serializer_class=serializers.BookListSerializer
    queryset=Book.objects.all()
    filterset_fields={
        'genre_name':['exact'],
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


        

class BookView(ModelViewSet):
    permission_classes=[AllowAny,]
    serializer_class=serializers.BookSerializer
    queryset=Book.objects.all()

    @extend_schema(
        responses={200: serializer_class},
        methods=['GET'],
        tags=['Book Overview']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class BookFavourite(ModelViewSet):
    permission_classes=[IsAuthenticated,]
    serializer_class=serializers.BookSerializer
    queryset=Book.objects.all()

    @extend_schema(
        responses={200: serializer_class},
        methods=['PUT'],
        tags=['Book Overview']
    )
    def update(self, request,pk):
        book=get_object_or_404(Book.objects.all(),pk=pk)
        book.users.add=request.user
        book.save()
        serializer=serializers.BookSerializer(book)
        return Response(serializer.data,status=status.HTTP_200_OK)

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