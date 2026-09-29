from django.conf import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название курса')
    preview = models.ImageField(upload_to='materials/courses/', blank=True, null=True, verbose_name='Превью (картинка)')
    description = models.TextField(blank=True, null=True, verbose_name='Описание курса')

    # Задание 3: Связь с владельцем курса
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name='Владелец')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название урока')
    description = models.TextField(blank=True, null=True, verbose_name='Описание урока')
    preview = models.ImageField(upload_to='materials/lessons/', blank=True, null=True, verbose_name='Превью (картинка)')
    video_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')

    # Задание 3: Связь с владельцем урока
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name='Владелец')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Курс')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        # Гарантируем уникальность пары пользователь-курс
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user.email} подписан на {self.course.title}'
