from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User


@shared_task
def check_inactive_users():
    """Периодическая задача: блокировка пользователей, не заходивших более месяца.
    Обновление происходит батчем (bulk update)."""
    one_month_ago = timezone.now() - timedelta(days=30)

    # Выбираем активных пользователей, у которых last_login был более 30 дней назад
    # Исключаем суперпользователей, чтобы случайно не заблокировать админку
    inactive_users = User.objects.filter(
        last_login__lte=one_month_ago,
        is_active=True,
        is_superuser=False
    )

    count = inactive_users.count()
    if count > 0:
        # Выполняем батч-апдейт (одним SQL-запросом к базе данных)
        inactive_users.update(is_active=False)
        return f"Заблокировано неактивных пользователей: {count}"

    return "Все пользователи активны."
