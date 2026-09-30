from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка метаданных для Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Онлайн Обучение API",
      default_version='v1',
      description="Документация для платформы онлайн-курсов и уроков",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),  # Доступно всем без авторизации
)

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('admin/', admin.site.urls),

    path('materials/', include('materials.urls', namespace='materials')),
    path('users/', include('users.urls', namespace='users')),

    # Задание 1: Эндпоинты для работы с JWT-токенами
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# Эндпоинты документации
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
