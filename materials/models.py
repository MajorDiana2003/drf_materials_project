from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название курса')
    preview = models.ImageField(
        upload_to='materials/courses/', blank=True, null=True, verbose_name='Превью (картинка)'
    )
    description = models.TextField(blank=True, null=True, verbose_name='Описание курса')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название урока')
    description = models.TextField(blank=True, null=True, verbose_name='Описание урока')
    preview = models.ImageField(
        upload_to='materials/lessons/', blank=True, null=True, verbose_name='Превью (картинка)'
    )
    video_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')

    # Связь с курсом. При удалении курса удалятся и его уроки (CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title
