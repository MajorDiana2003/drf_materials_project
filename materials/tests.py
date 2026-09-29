from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from materials.models import Course, Lesson, Subscription

class MaterialTestCase(APITestCase):

    def setUp(self):
        """Заполнение базы данных тестовыми объектами"""
        self.user = User.objects.create_user(email="test@example.com", password="password123")
        self.course = Course.objects.create(title="Тестовый курс", description="Описание курса", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            course=self.course,
            video_url="https://youtube.com",
            owner=self.user
        )
        # Принудительно авторизуем нашего тестового пользователя во внутреннем клиенте
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тест создания урока (с валидной ссылкой)"""
        url = reverse('materials:lesson-create')
        data = {
            "title": "Новый урок через тест",
            "course": self.course.id,
            "video_url": "https://youtube.com"
        }
        response = self.client.post(url, data=data)

        print("\nОШИБКА ВАЛИДАЦИИ:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_invalid_url(self):
        """Тест валидатора: попытка добавить ссылку не на youtube"""
        url = reverse('materials:lesson-create')
        data = {
            "title": "Невалидный урок",
            "course": self.course.id,
            "video_url": "https://rutube.ru"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_url', response.data)

    def test_get_lessons_list(self):
        """Тест получения списка уроков"""
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Так как работает пагинатор, структура ответа меняется (данные лежат в ключе 'results')
        self.assertIn('results', response.data)

    def test_get_lesson_detail(self):
        """Тест получения детальной информации об уроке"""
        url = reverse('materials:lesson-get', kwargs={"pk": self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_update_lesson(self):
        """Тест редактирования урока"""
        url = reverse('materials:lesson-update', kwargs={"pk": self.lesson.pk})
        data = {"title": "Обновленное название теста"}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Обновленное название теста")

    def test_delete_lesson(self):
        """Тест удаления урока"""
        url = reverse('materials:lesson-delete', kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_subscription_toggle(self):
        """Тест функционала подписки (добавление и удаление одной командой)"""
        url = reverse('materials:course-subscribe')
        data = {"course": self.course.id}

        # 1. Первый запрос должен создать подписку
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка на обновления курса успешно добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # 2. Повторный запрос должен её удалить
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка на обновления курса успешно удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

