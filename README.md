# Proxy Access Service

Сервис для управления доступом пользователей к виртуальным машинам (VM) через ключи активации.

Проект выполнен на:

- FastAPI
- PostgreSQL
- SQLAlchemy
- Redis
- Celery
- Docker
- Vue 3
- JWT Authentication
- WebSocket
- Pytest

---

# Возможности проекта

### Авторизация и пользователи

✅ Регистрация пользователя

✅ Авторизация по JWT

✅ Смена пароля

✅ Личный кабинет

✅ Logout

---

### Работа с ключами

✅ Генерация activation key

✅ Обновление ключа

✅ Отправка ключа на email через Celery

---

### Работа с VM

✅ Просмотр списка VM

✅ Назначение свободной VM пользователю

✅ Автоматическое освобождение VM

✅ Отображение статуса подключения

---

### Реальное время

✅ WebSocket подключение

✅ Отображение состояния подключения

---

### Инфраструктура

✅ Docker

✅ Docker Compose

✅ Redis

✅ PostgreSQL

✅ Celery Worker

✅ Celery Beat

---

### Тесты

Pytest:

```bash
docker compose exec backend python -m pytest
```

Пройдено:

```text
3 passed
```

---

# Запуск проекта

## Клонирование

```bash
git clone https://github.com/YOUR_USERNAME/proxy-access-service.git

cd proxy-access-service
```

---

## Создать .env

Пример:

```env
DATABASE_URL=postgresql://admin:admin@postgres_db:5432/proxy_db

SECRET_KEY=supersecretkey
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

REDIS_URL=redis://redis:6379/0

VM_TIMEOUT_MINUTES=30

SMTP_HOST=smtp.mail.ru
SMTP_PORT=465

SMTP_USER=your_email@mail.ru
SMTP_PASSWORD=app_password

EMAIL_FROM=your_email@mail.ru
```

---

## Запуск

Собрать контейнеры:

```bash
docker compose up --build
```

Остановить:

```bash
docker compose down
```

---

# Адреса

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Frontend:

```text
http://localhost:5173
```

---

# Структура проекта

```text
backend/
    app/
    tests/
    requirements.txt

frontend/
    src/

docker-compose.yml
README.md
```

---

# Автор

Карина

Проект выполнен как тестовое задание на позицию Backend Developer.