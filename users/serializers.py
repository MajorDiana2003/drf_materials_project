from rest_framework import serializers
from users.models import User, Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('user', 'session_id', 'payment_link')


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'payments', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Чтобы хэш пароля никогда не улетал в GET-ответах
        }

    def create(self, validated_data):
        """Обеспечивает хэширование пароля при регистрации через API"""
        user = User.objects.create_user(**validated_data)
        return user


class UserPublicSerializer(serializers.ModelSerializer):
    """Дополнительное задание: Ограниченный сериализатор для просмотра чужого профиля"""
    class Meta:
        model = User
        # Исключены: пароль, фамилия (в AbstractUser это last_name), история платежей
        fields = ['id', 'email', 'phone', 'city', 'avatar']

