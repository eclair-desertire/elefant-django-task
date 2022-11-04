from django.urls import path
from apps.catalog.views import common

urlpatterns=[
    path('register/',common.RegisterUserView.as_view()),
    path('token/',common.TokenObtainPairView.as_view()),
    path('token/refresh/',common.TokenRefreshView.as_view()),
    path('users/me/',common.SelfView.as_view({'get':'get'})),
    path('logout/',common.LogoutFormView.as_view()),
]