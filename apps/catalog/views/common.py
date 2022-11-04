from apps.catalog import serializers
from apps.catalog.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework import status, generics
from drf_spectacular.utils import extend_schema
from apps.catalog.models import User
from rest_framework.viewsets import ModelViewSet

class TokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer


class TokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer

class LogoutFormView(APIView):
    permission_classes=[AllowAny,]
    serializer_class=serializers.UserSerializer
    
    @extend_schema(
        responses={200: serializer_class},
        methods=['GET']
    )
    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

class RegisterUserView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=serializers.UserSerializer

    @extend_schema(
        request=serializer_class,
        responses={200: serializer_class},
        methods=['POST']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class SelfView(ModelViewSet):
    permission_classes=[AllowAny,]
    queryset=User.objects.all()
    serializer_class=serializers.UserSerializer

    @extend_schema(
        responses={200: serializer_class},
        methods=['GET'],
        tags=['Self Information']
    )
    def get(self,request):
        serializer=serializers.UserSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)