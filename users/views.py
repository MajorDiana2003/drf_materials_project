from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User, Payment
from users.serializers import UserSerializer, UserPublicSerializer, PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.services import (create_stripe_product, create_stripe_price,
                            create_stripe_session, retrieve_stripe_session
                            )


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


class PaymentCreateAPIView(generics.CreateAPIView):
    """Создание платежа через Stripe и генерация ссылки на оплату"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user, payment_method=Payment.TRANSFER)

        # Определяем имя продукта (курс или урок)
        product_name = payment.course.title if payment.course else payment.lesson.title

        # Интеграция со Stripe через сервисный слой
        product_id = create_stripe_product(product_name)
        price_id = create_stripe_price(payment.payment_amount, product_id)
        session_id, payment_link = create_stripe_session(price_id)

        # Сохраняем полученные ID сессии и ссылку в модель платежа
        payment.session_id = session_id
        payment.payment_link = payment_link
        payment.save()


class PaymentStatusAPIView(APIView):
    """Дополнительное задание: Проверка статуса платежа по ID сессии Stripe"""

    def get(self, request, session_id):
        payment_status = retrieve_stripe_session(session_id)
        return Response({"payment_status": payment_status})
