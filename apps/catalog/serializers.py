from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer, TokenObtainPairSerializer
)
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from apps.catalog.models import User
from rest_framework.pagination import PageNumberPagination

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

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('id','username','password','fav_books','reviews')
        extra_kwargs={
            'fav_books':{'required':False},
            'reviews':{'required':False},
        }

    def save(self):
        password = self.validated_data.pop('password', None)
        if password:
            self.validated_data['password'] = make_password(password)

        return super().save()
