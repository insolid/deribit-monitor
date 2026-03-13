## Описание
API для мониторинга курсов валют. Данные берутся из биржи Deribit.

## Запуск
1. Склонировать репозиторий
```bash
git clone https://github.com/insolid/deribit-monitor.git
```
2. Создать в корне проекта файл **.env**, скопировать туда переменные из **.env.example** и заполнить их своими значениями. Либо можно просто вставить:
```
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=deribit-monitor
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379
```
3. Из корня проекта выполнить команду
```bash
docker compose up
```
Swagger: http://localhost:8000/docs

Запуск тестов:
```
docker compose run --rm web pytest -s
```

## Стек
- FastAPI
- Celery
- SQLAlchemy + Alembic
- Postgresql
- Docker
