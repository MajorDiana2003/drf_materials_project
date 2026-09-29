import os
from celery import Celery

# Устанавливаем дефолтный модуль настроек Django для celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('drf_materials_project')

# Читаем конфигурацию
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем задачи
app.autodiscover_tasks()
