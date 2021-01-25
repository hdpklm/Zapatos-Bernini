from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions
from django.contrib.auth import login, logout
from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            errors = []
            print("error", serializer.errors)
            for item in serializer.errors:
                print(item, serializer.errors.get(item)[0])
                errors.append(f'{item}: {serializer.errors.get(item)[0]}')
            return Response({'error': errors})

        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class LogoutAPI(KnoxLogoutView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        logout(request)
        # super(LogoutAPI, self).post(request, format=None)
        return Response({"logout": "1"})
