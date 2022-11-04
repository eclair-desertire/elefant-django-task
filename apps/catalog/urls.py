from django.urls import path
from apps.catalog.views import common,books

urlpatterns=[
    path('register/',common.RegisterUserView.as_view()),
    path('token/',common.TokenObtainPairView.as_view()),
    path('token/refresh/',common.TokenRefreshView.as_view()),
    path('users/me/',common.SelfView.as_view({'get':'get'})),
    path('logout/',common.LogoutFormView.as_view()),

    path('books/',books.BooksListView.as_view({'get':'list'})),
    path('book/<int:pk>/',books.BookView.as_view({'get':'retrieve'})),
]