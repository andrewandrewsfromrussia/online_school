# Online School — Django + DRF

Учебный проект, реализующий базовый функционал онлайн-школы: кастомный пользователь (логин по email), курсы, уроки, платежи, JWT-авторизация и разграничение прав доступа.

## Стек технологий

* Python 3.11+
* Django
* Django REST Framework
* djangorestframework-simplejwt
* django-filter
* Poetry
* SQLite
* Pillow

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

### JWT-авторизация

* `POST /api/token/` – получение токенов
* `POST /api/token/refresh/` – обновление

---

## Пользователи и профили

* Регистрация: `POST /api/register/`
* Профиль: `GET/PUT/PATCH /api/profile/<id>/`
* Чужой профиль — урезанный вид (`PublicUserSerializer`)
* Свой профиль — полный (`UserSerializer`)

---

## Роли и группы

* Группа `moderators`
* Пермишены:  
  * `IsModer` — модератор  
  * `IsOwner` — владелец объекта  
  * `IsSelfOrReadOnly` — для профилей

---

## Курсы и уроки

### Курсы (CourseViewSet)

* Модератор: может list/retrieve/update, НЕ может create/delete  
* Пользователь: видит только свои; create/update/delete — только свои

### Уроки

* ListCreateView + RetrieveUpdateDestroyView  
* Логика аналогична курсам

---

## Платежи

* `PaymentViewSet`
* Фильтры: курс, урок, способ оплаты
* Сортировка по дате

---

## Админ-панель

* `/admin/`
* Пользователи + группы доступны для редактирования

---

## Резюме прав доступа

* Все API защищены авторизацией
* JWT + SessionAuth
* Модераторы — только просмотр/редактирование любых курсов/уроков
* Пользователи — только свои объекты
* Профили: смотреть — все, редактировать — только свой

