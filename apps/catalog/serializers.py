from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer, TokenObtainPairSerializer
)
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from apps.catalog.models import User, Book, Review, Genre
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

class TokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, *args, **kwargs):
        data = super().validate(*args, **kwargs)

        if not self.user.is_active:
            raise AuthenticationFailed({
                'detail': f"Пользователь {self.user.username} был деактивирован!"
            }, code='user_deleted')

        data['id'] = self.user.id
        data['username'] = self.user.username

        return data

class TokenRefreshSerializer(TokenRefreshSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])

        try:
            user = User.objects.get(
                pk=refresh.payload.get('user_id')
            )
        except ObjectDoesNotExist:
            raise serializers.ValidationError({
                'detail': f"Пользователь был удалён!"
            }, code='user_does_not_exists')

        if not user.is_active:
            raise AuthenticationFailed({
                'detail': f"Пользователь {user.username} был архивирован!"
            }, code='user_deleted')

        data['id'] = user.id
        data['username'] = user.username

        access = AccessToken(data['access'])

        return data

class Pagination(PageNumberPagination):

    class Meta:
        ordering = ['-id']

    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'page': self.page.number,
            'results': data
        })

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model=Review
        fields=('review_id','book_id','explanation','rate')
        extra_kwargs={
            'review_id':{'required':False},
        }
    
    def create(self, validated_data):
        instance=super().create(validated_data)
        print(self.context)
        print('*'*50)
        book=get_object_or_404(Book.objects.all(),pk=validated_data.get('book_id'))
        instance.books.add(book)
        instance.users.add(self.context.get('request').user)
        return super().create(validated_data)



class BookSerializer(serializers.ModelSerializer):
    
    reviews=ReviewSerializer(many=True,required=False)
    class Meta:
        model=Book
        fields=('book_id','book_name','genre_name',
            'author','description','published_date',
            'avg_rate','reviews')

        extra_kwargs={
            'genre_name':{'required':False},
            'published_date':{'required':False},
            'reviews':{'required':False},
        }


class UserSerializer(serializers.ModelSerializer):
    books=BookSerializer(many=True, required=False)
    reviews=ReviewSerializer(many=True,required=False)
    
    password = serializers.CharField(
        max_length=255,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('id','username','password','reviews','books')
        extra_kwargs={
            'reviews':{'required':False},
            'books':{'required':False},
        }

    def save(self):
        password = self.validated_data.pop('password', None)
        if password:
            self.validated_data['password'] = make_password(password)

        return super().save()

class BookListSerializer(serializers.ModelSerializer):
    #genre_name=serializers.CharField(source='genre.genre',read_only=True)

    class Meta:
        model=Book
        fields=('book_name','genre_name','author','avg_rate',)
    




class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model=Genre
        fields=('__all__')

