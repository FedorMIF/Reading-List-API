# Reading List API

REST API сервис для управления списком чтения (книги и статьи) с поддержкой тегов, фильтрации и пагинации.

## Возможности

- CRUD операции для элементов списка чтения (Item)
- Фильтрация по статусу, типу, приоритету, тегам, дате создания, подстроке в названии
- Пагинация (limit/offset) и сортировка
- Управление тегами: создание, привязка/отвязка к элементам
- Поддержка нескольких пользователей
- JSON API с обработкой ошибок
- Автоматическая документация (Swagger UI)

## Требования

- Python 3.10+
- pip

## Установка и запуск

### Вариант 1: Локальный запуск (рекомендуется для разработки)

#### 1. Клонирование репозитория (или распаковка архива)

```bash
cd /path/to/project
```

#### 2. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

#### 4. Конфигурация

По умолчанию используется SQLite. Для изменения настроек создайте файл `.env`:

```bash
cp .env.example .env
```

Отредактируйте `.env` при необходимости:

```env
DATABASE_URL=sqlite:///./reading_list.db
API_HOST=0.0.0.0
API_PORT=8000
```

Для PostgreSQL измените `DATABASE_URL`:
```env
DATABASE_URL=postgresql://user:password@localhost/reading_list
```

#### 5. Загрузка тестовых данных

```bash
python seed_data.py
```

Это создаст:
- 2 пользователя (Alice и Bob)
- 8 элементов списка чтения (книги и статьи)
- 7 тегов

#### 6. Запуск сервера

```bash
#готовый скрипт
./run.sh

#запуск вручную
python -m app.main

#через uvicorn с hot reload
uvicorn app.main:app --reload
```

Сервер будет доступен по адресу: `http://localhost:8000`

### Вариант 2: Docker (рекомендуется для продакшена)

#### Запуск через Docker Compose

```bash
# Сборка и запуск
docker-compose up --build

# В фоновом режиме
docker-compose up -d

# Остановка
docker-compose down
```

#### Загрузка seed данных в Docker

```bash
docker-compose exec api python seed_data.py
```

#### Запуск через Docker напрямую

```bash
# Сборка образа
docker build -t reading-list-api .

# Запуск контейнера
docker run -p 8000:8000 -v $(pwd)/data:/app/data reading-list-api
```

## Документация API

После запуска сервера документация доступна по адресу:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Примеры запросов

### Базовые эндпоинты

#### Healthcheck
```bash
curl http://localhost:8000/health
```

### Items (Элементы списка чтения)

#### 1. Создать новый элемент

```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "title": "Design Patterns",
    "kind": "book",
    "status": "planned",
    "priority": "high",
    "notes": "Классика программирования",
    "tag_ids": [1, 3]
  }'
```

#### 2. Получить элемент по ID

```bash
curl http://localhost:8000/items/1
```

#### 3. Получить список элементов (базовый)

```bash
curl http://localhost:8000/items
```

#### 4. Список элементов с фильтрацией

**По статусу и типу:**
```bash
curl "http://localhost:8000/items?status=reading&kind=book"
```

**По приоритету:**
```bash
curl "http://localhost:8000/items?priority=high"
```

**По пользователю:**
```bash
curl "http://localhost:8000/items?user_id=1"
```

**По тегам (любой из):**
```bash
curl "http://localhost:8000/items?tag_ids=1,2"
```

**По подстроке в названии:**
```bash
curl "http://localhost:8000/items?title_contains=python"
```

**По диапазону дат:**
```bash
curl "http://localhost:8000/items?created_after=2024-01-01T00:00:00&created_before=2024-12-31T23:59:59"
```

**Комбинированные фильтры:**
```bash
curl "http://localhost:8000/items?user_id=1&status=reading&priority=high&title_contains=python"
```

#### 5. Пагинация и сортировка

**Пагинация:**
```bash
curl "http://localhost:8000/items?limit=10&offset=0"
```

**Сортировка по дате создания (по убыванию):**
```bash
curl "http://localhost:8000/items?sort_by=created_at&sort_order=desc"
```

**Сортировка по дате обновления (по возрастанию):**
```bash
curl "http://localhost:8000/items?sort_by=updated_at&sort_order=asc"
```

**Сортировка по приоритету:**
```bash
curl "http://localhost:8000/items?sort_by=priority&sort_order=desc"
```

**Комбинация фильтров, пагинации и сортировки:**
```bash
curl "http://localhost:8000/items?user_id=1&status=reading&sort_by=priority&sort_order=desc&limit=5&offset=0"
```

#### 6. Обновить элемент

```bash
curl -X PATCH "http://localhost:8000/items/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "reading",
    "notes": "Начал читать, очень интересно!"
  }'
```

#### 7. Удалить элемент

```bash
curl -X DELETE "http://localhost:8000/items/1"
```

#### 8. Добавить теги к элементу

```bash
curl -X POST "http://localhost:8000/items/1/tags" \
  -H "Content-Type: application/json" \
  -d '{
    "tag_ids": [2, 3]
  }'
```

#### 9. Удалить теги из элемента

```bash
curl -X DELETE "http://localhost:8000/items/1/tags" \
  -H "Content-Type: application/json" \
  -d '{
    "tag_ids": [2]
  }'
```

### Tags (Теги)

#### 1. Создать тег

```bash
curl -X POST "http://localhost:8000/tags" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "name": "javascript"
  }'
```

#### 2. Получить список тегов

```bash
curl "http://localhost:8000/tags"
```

**С фильтрацией по пользователю:**
```bash
curl "http://localhost:8000/tags?user_id=1"
```

**Поиск по подстроке в имени:**
```bash
curl "http://localhost:8000/tags?name_contains=python"
```

#### 3. Получить тег по ID

```bash
curl "http://localhost:8000/tags/1"
```

#### 4. Удалить тег

```bash
curl -X DELETE "http://localhost:8000/tags/1"
```

## Структура проекта

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # Главный файл приложения
│   ├── config.py            # Конфигурация
│   ├── database.py          # Настройка БД
│   ├── models/              # SQLAlchemy модели
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── item.py
│   │   ├── tag.py
│   │   └── item_tag.py      # M2M связь
│   ├── schemas/             # Pydantic схемы
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── item.py
│   │   └── tag.py
│   └── routers/             # API endpoints
│       ├── __init__.py
│       ├── items.py
│       └── tags.py
├── alembic/                 # Миграции (опционально)
│   ├── env.py
│   └── ...
├── alembic.ini
├── requirements.txt
├── seed_data.py            # Скрипт загрузки тестовых данных
├── .env.example            # Пример конфигурации
├── .gitignore
└── README.md
```

## Модель данных

### User (Пользователь)
- `id` (integer, PK)
- `email` (string, unique)
- `display_name` (string)
- `created_at` (datetime)

### Item (Элемент списка чтения)
- `id` (integer, PK)
- `user_id` (integer, FK → users.id)
- `title` (string)
- `kind` (enum: "book" | "article")
- `status` (enum: "planned" | "reading" | "done")
- `priority` (enum: "low" | "normal" | "high")
- `notes` (text, nullable)
- `created_at` (datetime)
- `updated_at` (datetime)

### Tag (Тег)
- `id` (integer, PK)
- `user_id` (integer, FK → users.id)
- `name` (string)
- Уникальное ограничение: (user_id, name)

### item_tags (M2M связь)
- `item_id` (integer, FK → items.id)
- `tag_id` (integer, FK → tags.id)

## Основные решения и допущения

### Архитектурные решения

1. **Структура проекта**: Разделение на слои (models, schemas, routers) для читаемости и масштабируемости
2. **ORM**: Использование SQLAlchemy для работы с БД (легко переключиться с SQLite на PostgreSQL)
3. **Валидация**: Pydantic для валидации входных данных и сериализации ответов
4. **База данных**: SQLite по умолчанию для простоты разработки и демонстрации

### Упрощения

1. **Аутентификация**: Не реализована. В production добавить JWT/OAuth2
2. **Авторизация**: Нет проверки прав доступа (пользователь может видеть чужие items)
3. **Миграции**: Alembic настроен, но таблицы создаются автоматически через `Base.metadata.create_all()`
4. **Валидация user_id**: Не проверяется существование пользователя при создании Item
5. **Тестирование**: Автоматические тесты не включены (в production добавить pytest)

### Production-ready улучшения

Для использования в продакшене рекомендуется добавить:

1. **Безопасность**:
   - JWT аутентификацию
   - Rate limiting
   - CORS настройки
   - Валидацию прав доступа

2. **Масштабируемость**:
   - Кеширование (Redis)
   - Асинхронные операции
   - Connection pooling

3. **Мониторинг**:
   - Логирование (structured logging)
   - Метрики (Prometheus)
   - APM (Application Performance Monitoring)

4. **Тестирование**:
   - Unit тесты
   - Integration тесты
   - E2E тесты

5. **DevOps**:
   - Docker/Docker Compose
   - CI/CD pipeline
   - Kubernetes манифесты

## Обработка ошибок

API возвращает ошибки в формате JSON:

```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "details": {}
}
```

Коды ошибок:
- `404` - Ресурс не найден
- `422` - Ошибка валидации
- `400` - Некорректный запрос
- `500` - Внутренняя ошибка сервера

## Тестовые данные

После запуска `seed_data.py` в БД будут созданы:

**Пользователи:**
1. Alice Reader (alice@example.com) - 5 элементов, 4 тега
2. Bob Bookworm (bob@example.com) - 3 элемента, 3 тега

**Элементы с разными статусами:**
- `planned`: 2
- `reading`: 3
- `done`: 3

**Приоритеты:**
- `high`: 4
- `normal`: 3
- `low`: 1

**Типы:**
- `book`: 5
- `article`: 3

## Миграции (опционально)

Проект настроен для работы с Alembic, но таблицы создаются автоматически.

Для использования миграций:

```bash
# Создать миграцию
alembic revision --autogenerate -m "Initial migration"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1
```

## Поддержка

При возникновении проблем проверьте:
1. Установлены ли все зависимости из `requirements.txt`
2. Загружены ли seed данные
3. Доступен ли порт 8000
4. Корректен ли формат JSON в запросах

## Дополнительные файлы

Проект включает вспомогательные скрипты для удобства:

- `run.sh` - Скрипт быстрого запуска сервера
- `examples.sh` - Скрипт с примерами всех типов запросов
- `QUICKSTART.md` - Краткое руководство для быстрого старта
- `docker-compose.yml` - Конфигурация для Docker
- `Dockerfile` - Образ Docker для контейнеризации

### Использование скриптов

```bash
# Запуск сервера
./run.sh

# Выполнение примеров запросов (сервер должен быть запущен)
./examples.sh
```

## Структура ответов API

Все успешные ответы имеют единообразную структуру:

**Одиночный объект:**
```json
{
  "data": { /* объект */ }
}
```

**Список объектов:**
```json
{
  "data": [ /* массив объектов */ ],
  "total": 10,
  "limit": 50,
  "offset": 0
}
```

## Лицензия

MIT

# Reading-List-API
