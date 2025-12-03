# Online School — Django + DRF

Учебный проект, реализующий функционал онлайн‑школы: кастомный пользователь (логин по email), курсы, уроки, подписки, платежи, JWT‑авторизация и разграничение прав доступа.

---

## Стек технологий

- Python 3.11+
- Django
- Django REST Framework
- djangorestframework-simplejwt
- django-filter
- Poetry
- SQLite
- Pillow

---

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <URL-репозитория>
cd online_school
```

### 2. Установка зависимостей

```bash
poetry install
```

### 3. Активация окружения

```bash
poetry env activate
```

### 4. Применение миграций

```bash
poetry run python manage.py migrate
```

### 5. Создание суперпользователя

```bash
poetry run python manage.py createsuperuser
```

### 6. Запуск сервера разработки

```bash
poetry run python manage.py runserver
```

---

## Аутентификация и авторизация

### JWT‑авторизация

- `POST /api/token/` – получение токенов
- `POST /api/token/refresh/` – обновление токена

---

## Пользователи и профили

- Регистрация: `POST /api/register/`
- Профиль: `GET/PUT/PATCH /api/profile/<id>/`
- Чужой профиль — ограниченный (`PublicUserSerializer`)
- Свой профиль — полный (`UserSerializer`)

---

## Роли и группы

- Группа `moderators`
- Пермишены:
  - `IsModer` — модератор
  - `IsOwner` — владелец объекта
  - `IsSelfOrReadOnly` — только для собственных профилей

---

## Курсы и уроки

### Курсы (`CourseViewSet`)

- Пользователь:
  - видит только свои курсы
  - может создавать, обновлять, удалять только свои
- Модератор:
  - может просматривать любые курсы
  - НЕ может создавать и удалять

### Уроки

- `LessonListCreateView` — список и создание
- `LessonRetrieveUpdateDestroyView` — просмотр, редактирование, удаление

Права доступа аналогичны курсам:
- пользователь работает только со своими
- модератор видит любые, но не создаёт и не удаляет

---

## Подписки на курсы

Пользователь может подписаться на обновления курса.

### Эндпоинт:
```
POST /lms/subscriptions/toggle/
{
  "course_id": <id курса>
}
```

### Логика:
- при отсутствии подписки → создаётся
- при наличии → удаляется

### В курсах возвращается поле:
```
"is_subscribed": true/false
```

---

## Валидация материалов урока

Видео‑ссылки допускаются **только с YouTube** — `youtube.com` или `youtu.be`.

Любые другие домены отклоняются.

---

## Пагинация

В `paginators.py` реализованы:
- `CoursePagination`
- `LessonPagination`

Параметры:
- `page_size`
- `page_size_query_param`
- `max_page_size`

Используются в соответствующих вью.

---

## Тестирование

Написано 19 тестов, покрывающих:

- CRUD уроков
- права владельца / модератора / анонимного пользователя
- валидацию YouTube‑ссылок
- механику подписок
- поле `is_subscribed`

### Результат покрытия:

```
Name                                               Stmts   Miss  Cover
----------------------------------------------------------------------
lms\__init__.py                                        0      0   100%
lms\admin.py                                           1      0   100%
lms\apps.py                                            4      0   100%
lms\migrations\0001_initial.py                         6      0   100%
lms\migrations\0002_course_owner_lesson_owner.py       6      0   100%
lms\migrations\0003_subscription.py                    6      0   100%
lms\migrations\__init__.py                             0      0   100%
lms\models.py                                         27      3    89%
lms\paginators.py                                      9      0   100%
lms\permissions.py                                     8      0   100%
lms\serializers.py                                    23      1    96%
lms\tests.py                                         129      0   100%
lms\urls.py                                            7      0   100%
lms\validators.py                                     10      1    90%
lms\views.py                                          67      5    93%
----------------------------------------------------------------------
TOTAL                                                303     10    97%
```

---