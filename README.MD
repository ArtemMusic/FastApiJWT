### Что было сделано
1) Полный асинхронный CRUD пользователей в postgresql
2) Нативное создание jwt токенов (access, refresh) и авторизация через jwt


### Инструкция по запуску

1) Сгенерировать приватный ключ через команду
    `openssl genrsa -out jwt-private.pem 2048`
2) Сгенерировать публичный ключ через команду
    `openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem`
3) Сохдать .env файл:
`DB_HOST=localhost (изменить на свой ip контейнера postgresql)
DB_PORT=5432
DB_NAME=fastapijwt
DB_USER=root
DB_PASS=root`
4) Запустить файл docker-compose для контейнера с postgresql.
5) Сделать миграции бд через alembic: 1) `alembic revision --autogenerate -m 'create user table'` 2) `alembic upgrade head`

### Что было использовано
1) python
2) fastapi
3) SQLAlchemy + asyncio
4) pydantic
5) alembic
6) pyjwt + crypto
7) asyncpg