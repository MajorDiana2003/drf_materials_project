from rest_framework import serializers
from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    # Задание 1: Поле для подсчета количества уроков через SerializerMethodField
    lessons_count = serializers.SerializerMethodField()

    # Задание 3: Вложенный сериализатор для вывода информации по всем урокам курса
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lessons_count', 'lessons']

    # Метод для подсчета уроков
    def get_lessons_count(self, obj):
        return obj.lessons.count()
