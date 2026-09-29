from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from materials.models import Course, Lesson, Subscription
from materials.serializers import CourseSerializer, LessonSerializer
from materials.permissions import IsModerator, IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from materials.paginators import MaterialPagination

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialPagination

    def get_permissions(self):
        """Задание 2 и 3: Динамическое распределение прав для курсов"""
        if self.action == 'create':
            # Модератор не может создавать курсы
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            # Модератор или Владелец могут просматривать и редактировать
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            # Модератор не может удалять, удаляет только Владелец
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Автоматическое сохранение владельца при создании курса"""
        serializer.save(owner=self.request.user)


# Дженерики для Уроков с разграничением прав
class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]  # Модератор не может создавать

    def perform_create(self, serializer):
        """Автоматическое сохранение владельца при создании урока"""
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]  # Модератор или Владелец


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]  # Модератор или Владелец


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]  # Только Владелец (Модератор не может)


class SubscriptionAPIView(APIView):
    """Управление подпиской на обновления курса (Добавление/Удаление)"""
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')
        course_item = get_object_or_404(Course, id=course_id)

        # Ищем подписку в базе данных
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            # Если подписка существует — удаляем её
            subs_item.delete()
            message = 'Подписка на обновления курса успешно удалена'
        else:
            # Если подписки нет — создаем её
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка на обновления курса успешно добавлена'

        return Response({"message": message})