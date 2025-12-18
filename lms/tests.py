from django.contrib.auth.models import Group
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from lms.models import Course, Lesson, Subscription


User = get_user_model()


class LessonAPITestCase(APITestCase):
    def setUp(self):
        # Группа модераторов
        self.moderators_group, _ = Group.objects.get_or_create(name="moderators")

        # Обычный пользователь
        self.user = User.objects.create_user(
            email="user@example.com",
            password="password123",
        )

        # Модератор
        self.moderator = User.objects.create_user(
            email="moder@example.com",
            password="password123",
        )
        self.moderator.groups.add(self.moderators_group)

        # Другой пользователь
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="password123",
        )

        # Курс
        self.course = Course.objects.create(
            title="Test course",
            description="Test course description",
            owner=self.user,
        )

        # Уроки: два принадлежат self.user, один — другому пользователю
        self.lesson1 = Lesson.objects.create(
            title="Lesson 1",
            description="Desc 1",
            owner=self.user,
            course=self.course,
        )
        self.lesson2 = Lesson.objects.create(
            title="Lesson 2",
            description="Desc 2",
            owner=self.user,
            course=self.course,
        )
        self.foreign_lesson = Lesson.objects.create(
            title="Foreign lesson",
            description="Foreign desc",
            owner=self.other_user,
            course=self.course,
        )

        # URL списка уроков
        self.lesson_list_url = reverse("lms:lesson-list-create")
        # detail-URL для lesson1
        self.lesson_detail_url = reverse("lms:lesson-detail", kwargs={"pk": self.lesson1.pk})

    # -------- LIST --------

    def test_lesson_list_for_owner(self):
        """Владелец видит только свои уроки."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.lesson_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data["results"]]

        self.assertIn("Lesson 1", titles)
        self.assertIn("Lesson 2", titles)
        self.assertNotIn("Foreign lesson", titles)

    def test_lesson_list_for_moderator_sees_all(self):
        """Модератор видит все уроки."""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(self.lesson_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data["results"]]

        self.assertIn("Lesson 1", titles)
        self.assertIn("Lesson 2", titles)
        self.assertIn("Foreign lesson", titles)

    def test_lesson_list_unauthenticated(self):
        """Неаутентифицированный пользователь не имеет доступа к списку уроков."""
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -------- CREATE --------

    def test_lesson_create_by_owner_success(self):
        """Обычный пользователь может создать урок."""
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "New lesson",
            "description": "New desc",
            "course": self.course.id,
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        }
        response = self.client.post(self.lesson_list_url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])
        new_lesson = Lesson.objects.get(id=response.data["id"])
        self.assertEqual(new_lesson.owner, self.user)

    def test_lesson_create_by_moderator_forbidden(self):
        """Модератор не может создавать уроки."""
        self.client.force_authenticate(user=self.moderator)
        payload = {
            "title": "Mod lesson",
            "description": "Mod desc",
            "course": self.course.id,
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        }
        response = self.client.post(self.lesson_list_url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_create_unauthenticated_forbidden(self):
        """Неаутентифицированный пользователь не может создавать уроки."""
        payload = {
            "title": "Anon lesson",
            "description": "Anon desc",
            "course": self.course.id,
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        }
        response = self.client.post(self.lesson_list_url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_create_with_non_youtube_link_fails(self):
        """Валидация video_url: не-YouTube ссылка должна быть отклонена."""
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "Bad link lesson",
            "description": "Bad link desc",
            "course": self.course.id,
            "video_url": "https://example.com/video",
        }
        response = self.client.post(self.lesson_list_url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("video_url", response.data)

    # -------- RETRIEVE --------

    def test_lesson_retrieve_owner(self):
        """Владелец может получить детальную информацию по своему уроку."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.lesson_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.lesson1.id)

    def test_lesson_retrieve_moderator(self):
        """Модератор может получить детальную информацию по любому уроку."""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(self.lesson_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.lesson1.id)

    def test_lesson_retrieve_foreign_user_forbidden(self):
        """Другой пользователь (не владелец и не модератор) не имеет доступа к детальному уроку."""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.lesson_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_retrieve_unauthenticated_forbidden(self):
        """Неаутентифицированный пользователь не имеет доступа к детальному уроку."""
        response = self.client.get(self.lesson_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -------- DELETE --------

    def test_lesson_delete_owner_success(self):
        """Владелец может удалить свой урок."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.lesson_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson1.id).exists())

    def test_lesson_delete_moderator_forbidden(self):
        """Модератор не может удалять уроки (DELETE доступен только владельцу)."""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(self.lesson_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_foreign_user_forbidden(self):
        """Другой пользователь не может удалить чужой урок."""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.lesson_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_unauthenticated_forbidden(self):
        """Неаутентифицированный пользователь не может удалить урок."""
        response = self.client.delete(self.lesson_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        # Группа модераторов (на всякий случай, для консистентности проекта)
        self.moderators_group, _ = Group.objects.get_or_create(name="moderators")

        self.user = User.objects.create_user(
            email="subuser@example.com",
            password="password123",
        )
        self.other_user = User.objects.create_user(
            email="subother@example.com",
            password="password123",
        )

        # Курс владельца self.user
        self.course = Course.objects.create(
            title="Subscription course",
            description="Course for subscription tests",
            owner=self.user,
        )
        self.course_detail_url = reverse("lms:courses-detail", kwargs={"pk": self.course.pk})

        # Курс владельца self.other_user
        self.other_course = Course.objects.create(
            title="Other user course",
            description="Course for other user",
            owner=self.other_user,
        )
        self.other_course_detail_url = reverse("lms:courses-detail", kwargs={"pk": self.other_course.pk})

        # URL эндпоинта подписки
        self.subscription_url = reverse("lms:subscription-toggle")

    def test_subscription_toggle_add_and_remove(self):
        """Подписка создаётся и удаляется повторным вызовом."""
        self.client.force_authenticate(user=self.user)

        # Добавляем подписку
        response = self.client.post(
            self.subscription_url,
            data={"course_id": self.course.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Удаляем подписку
        response = self.client.post(
            self.subscription_url,
            data={"course_id": self.course.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_requires_authentication(self):
        """Неаутентифицированный пользователь не может управлять подпиской."""
        response = self.client.post(
            self.subscription_url,
            data={"course_id": self.course.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_subscribed_flag_true_for_subscribed_user(self):
        """Поле is_subscribed = True для пользователя с подпиской."""
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.course_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_subscribed"])

    def test_is_subscribed_flag_false_for_other_user(self):
        """Поле is_subscribed = False для пользователя без подписки на свой курс."""
        # Подписок у other_user нет
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.other_course_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_subscribed"])

