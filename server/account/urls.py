from .views import RegisterAPI
from django.urls import path
from knox import views as knox_views
from .views import LoginAPI, LogoutAPI
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('register/', RegisterAPI.as_view(), name='register'),
]
