# from django.shortcuts import render
from djoser.views import UserViewSet

from .models import User
from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
