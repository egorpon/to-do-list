# To-Do List API

REST API for todo lists and tasks.

```
Client -> Django API (:8000) -> PostgreSQL (:5432)
                              -> Redis (:6379)     [cache]
                              -> RabbitMQ (:5672) -> Celery worker/beat
```

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv)
- Docker + Docker Compose

## Setup

### 1. Copy environment file

```bash
cp .env.example .env
```

Fill in `POSTGRES_*`, `SECRET_KEY`, `EMAIL_HOST_*`, `CELERY_BROKER_URL`.

### 2. Start everything

```bash
docker compose up --build
```

Migrations run automatically on container start.

## Running

```bash
docker compose up
```

Open `http://localhost:8000/api/schema/swagger-ui/`.

## Project layout

```
todolist/
  api/v1/{todos,tasks}/   views, serializers, urls
  todos/                  models, selectors, services, signals
  tasks/                  models, selectors, services, signals
  async_tasks/            Celery app, periodic tasks, email notifications
```

Layers: `views` (parse/validate request) → `selectors` (reads) → `services` (writes, side effects).

## API

```
POST   /api/token/                        obtain JWT
GET    /api/v1/todos/                     list todo lists
POST   /api/v1/todos/create/              create
GET    /api/v1/todos/<id>/                detail
PATCH  /api/v1/todos/<id>/update/         update
DELETE /api/v1/todos/<id>/delete/         delete

GET    /api/v1/todos/<id>/tasks/          list tasks
POST   /api/v1/todos/<id>/tasks/create    create task
GET    /api/v1/tasks/<id>/                detail
PATCH  /api/v1/tasks/<id>/update          update
DELETE /api/v1/tasks/<id>/delete          delete
```

## Development

```bash
docker compose exec web python manage.py test          # run tests
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

## Commit convention

[Conventional Commits](https://www.conventionalcommits.org/): `feat(scope): ...`, `fix(scope): ...`, `perf(scope): ...`