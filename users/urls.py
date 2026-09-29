from django.urls import path
from users.apps import UsersConfig
from users.views import (UserCreateAPIView, UserListAPIView,
                         UserProfileUpdateAPIView, PaymentListAPIView,
                         PaymentCreateAPIView, PaymentStatusAPIView
                         )

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('', UserListAPIView.as_view(), name='user-list'),
    path('profile/<int:pk>/', UserProfileUpdateAPIView.as_view(), name='user-profile'), # вернули pk для поддержки просмотра других профилей по доп. заданию
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    # Новые пути для Stripe оплаты
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payments/status/<str:session_id>/', PaymentStatusAPIView.as_view(), name='payment-status'),
]


