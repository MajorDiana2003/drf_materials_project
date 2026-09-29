from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsOwner

class UserProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Просмотр и редактирование профиля пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

