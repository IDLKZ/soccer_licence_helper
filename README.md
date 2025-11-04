# License Helper Service

Профессиональный микросервис для генерации отчетов на основе Clean Architecture.

## Архитектура

Проект построен на принципах Clean Architecture с четким разделением слоев:

### Слои приложения

1. **Domain Layer** (`app/domain/`)
   - Entities: Бизнес-сущности
   - Repositories: Интерфейсы репозиториев
   - Services: Доменные сервисы

2. **Application Layer** (`app/application/`)
   - Use Cases: Сценарии использования
   - DTOs: Объекты передачи данных

3. **Infrastructure Layer** (`app/infrastructure/`)
   - Database: Реализация репозиториев и подключение к БД
   - External: Интеграции с внешними сервисами

4. **Presentation Layer** (`app/presentation/`)
   - API: REST API endpoints
   - Schemas: Pydantic схемы для валидации

5. **Core** (`app/core/`)
   - Config: Конфигурация приложения
   - Database: Настройка подключения к БД
   - Dependencies: Dependency Injection

## Технологический стек

- **Framework**: FastAPI
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Validation**: Pydantic V2
- **Testing**: Pytest

## Структура проекта

```
license_helper/
├── app/
│   ├── core/                    # Конфигурация и настройки
│   ├── domain/                  # Бизнес-логика
│   ├── application/             # Use cases
│   ├── infrastructure/          # Внешние зависимости
│   └── presentation/            # API слой
├── tests/                       # Тесты
├── alembic/                     # Миграции БД
├── docker-compose.yml           # Docker конфигурация
└── requirements.txt             # Зависимости
```

## Установка и запуск

### Локальная разработка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

4. Запустите MySQL через Docker:
```bash
docker-compose up -d mysql
```

5. Примените миграции:
```bash
alembic upgrade head
```

6. Запустите приложение:
```bash
uvicorn app.main:app --reload
```

### Docker

Запуск всего приложения в Docker:
```bash
docker-compose up --build
```

## API Документация

После запуска приложения документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Тестирование

Запуск тестов:
```bash
pytest
```

Запуск с покрытием:
```bash
pytest --cov=app tests/
```

## Принципы разработки

- **SOLID принципы**
- **Dependency Inversion**: Зависимости направлены к центру (domain)
- **Repository Pattern**: Абстракция доступа к данным
- **Use Case Pattern**: Изолированная бизнес-логика
- **Clean Architecture**: Независимость от фреймворков и БД

## Разработка

1. Все новые фичи начинаются с создания use case
2. Доменная логика не зависит от внешних слоев
3. Используйте dependency injection
4. Покрывайте код тестами
