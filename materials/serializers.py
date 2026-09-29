from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import validate_youtube_url

class LessonSerializer(serializers.ModelSerializer):
    # Привязываем валидатор непосредственно к полю
    video_url = serializers.URLField(validators=[validate_youtube_url], required=False, allow_null=True)

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('owner',)


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    # Поле признака подписки текущего пользователя
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lessons_count', 'lessons', 'is_subscribed']
        read_only_fields = ('owner',)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False


