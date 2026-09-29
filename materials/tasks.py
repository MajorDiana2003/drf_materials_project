from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from materials.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    """Асинхронная рассылка писем всем подписчикам курса об обновлении материалов"""
    try:
        course = Course.objects.get(id=course_id)
        # Находим все активные подписки на данный курс
        subscriptions = Subscription.objects.filter(course=course)

        # Собираем список email-адресов подписчиков
        recipient_list = [sub.user.email for sub in subscriptions if sub.user.email]

        if recipient_list:
            send_mail(
                subject=f'Обновление курса: {course.title}',
                message=f'Привет! Материалы курса "{course.title}" были обновлены. Заходи на платформу, чтобы изучить новые уроки!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            return f"Уведомление отправлено {len(recipient_list)} пользователям."
        return "Нет подписчиков для отправки."
    except Course.DoesNotExist:
        return f"Курс с ID {course_id} не найден."
