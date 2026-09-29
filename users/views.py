from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User, Payment
from users.serializers import UserSerializer, UserPublicSerializer, PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class UserCreateAPIView(generics.CreateAPIView):
    """Задание 1: Регистрация пользователей (Открыта для всех)"""
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserListAPIView(generics.ListAPIView):
    """Просмотр списка пользователей"""
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer  # Для списка отдаем только публичные данные


class UserProfileUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Задание 1 + Доп. задание: Просмотр, обновление и удаление пользователя"""
    queryset = User.objects.all()

    def get_serializer_class(self):
        """Если запрашивается свой профиль — отдаем полную инфу, если чужой — публичную"""
        if self.get_object() == self.request.user:
            return UserSerializer
        return UserPublicSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('payment_date',)

