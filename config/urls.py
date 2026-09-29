from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('admin/', admin.site.urls),
    # Подключаем маршруты приложений
    path('materials/', include('materials.urls', namespace='materials')),
    path('users/', include('users.urls', namespace='users')),
]
