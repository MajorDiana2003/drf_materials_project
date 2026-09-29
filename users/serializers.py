from rest_framework import serializers
from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # Дополнительное задание: выводим историю платежей пользователя
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        # Добавляем 'payments' в список выводимых полей
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'payments']
