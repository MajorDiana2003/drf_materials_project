from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer
from users.permissions import IsOwner
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class UserProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Просмотр и редактирование профиля пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        # Эндпоинт вернет того пользователя, который авторизован, независимо от pk в URL
        return self.request.user


class PaymentListAPIView(generics.ListAPIView):
    """Вывод списка платежей с фильтрацией и сортировкой"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ('course', 'lesson', 'payment_method')

    ordering_fields = ('payment_date',)
