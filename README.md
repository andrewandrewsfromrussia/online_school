# Online School — Django + DRF

Учебный проект, реализующий базовый функционал онлайн-школы: кастомный пользователь, курсы, уроки, API CRUD и минимальный веб-интерфейс.

## Стек технологий
- **Python 3.11+**
- **Django**
- **Django REST Framework**
- **Poetry**
- **SQLite**
- **Pillow**

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

### 6. Запуск сервера
```bash
poetry run python manage.py runserver
```
