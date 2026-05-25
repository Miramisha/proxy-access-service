# Сверка с ТЗ

## Было уже реализовано

- FastAPI backend
- SQLAlchemy-модели User и VirtualMachine
- PostgreSQL/Redis/Celery в docker-compose
- JWT-login
- Swagger через FastAPI `/docs`
- Базовые endpoints регистрации, логина, профиля, VM, ключей
- Celery beat для освобождения VM по timeout

## Доделано

- Исправлена регистрация frontend/backend: `password_confirm` теперь передаётся корректно.
- После регистрации показывается сообщение «Письмо с ключом отправлено на почту».
- Добавлен личный кабинет `/profile` / `/cabinet` с текущим ключом.
- Добавлена кнопка «Обновить ключ» с отправкой ключа через Celery.
- Добавлена смена пароля: `POST /api/users/change-password`.
- Добавлен обязательный endpoint из ТЗ `POST /api/activate-key`.
- Activation key стал одноразовым: после успешной активации удаляется.
- Добавлена проверка истечения ключа.
- Добавлена выдача первой свободной активной VM с блокировкой строки PostgreSQL.
- Добавлен WebSocket `/ws/connection-status/{user_id}/`.
- Добавлен desktop-клиент `desktop/desktop_client.py` с WebSocket-обновлением статуса.
- Frontend переведён на Vue 3 + Vuetify 3.
- README обновлён инструкциями запуска, регистрации, получения ключа и desktop.

## Что проверить вручную

1. `docker compose up -d --build`
2. `docker logs celery_worker` — убедиться, что ключ печатается в console email режиме.
3. Создать VM через Swagger.
4. Запустить desktop-клиент, вставить ключ и проверить подключение.
5. Проверить WebSocket в desktop-клиенте или через любой WS-клиент.
