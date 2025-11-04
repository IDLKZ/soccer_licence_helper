# Структура проекта License Helper Service

```
license_helper/
│
├── app/                                    # Основное приложение
│   ├── __init__.py
│   ├── main.py                            # Точка входа FastAPI приложения
│   │
│   ├── core/                              # Ядро инфраструктуры
│   │   ├── __init__.py
│   │   ├── config.py                      # Конфигурация приложения
│   │   ├── database.py                    # Настройка БД и сессий
│   │   └── dependencies.py                # Dependency Injection контейнер
│   │
│   ├── domain/                            # Domain Layer (Бизнес-логика)
│   │   ├── __init__.py
│   │   │
│   │   ├── entities/                      # Бизнес-сущности
│   │   │   ├── __init__.py
│   │   │   └── report.py                  # Entity: Report + Enums
│   │   │
│   │   ├── repositories/                  # Интерфейсы репозиториев
│   │   │   ├── __init__.py
│   │   │   └── report_repository.py       # Interface: IReportRepository
│   │   │
│   │   └── services/                      # Доменные сервисы
│   │       ├── __init__.py
│   │       └── report_service.py          # Service: ReportDomainService
│   │
│   ├── application/                       # Application Layer (Use Cases)
│   │   ├── __init__.py
│   │   │
│   │   ├── dto/                           # Data Transfer Objects
│   │   │   ├── __init__.py
│   │   │   └── report_dto.py              # DTOs для отчетов
│   │   │
│   │   └── use_cases/                     # Сценарии использования
│   │       ├── __init__.py
│   │       ├── create_report.py           # UseCase: Создание отчета
│   │       ├── generate_report.py         # UseCase: Генерация отчета
│   │       ├── get_report.py              # UseCase: Получение отчета
│   │       ├── list_reports.py            # UseCase: Список отчетов
│   │       └── delete_report.py           # UseCase: Удаление отчета
│   │
│   ├── infrastructure/                    # Infrastructure Layer (Реализации)
│   │   ├── __init__.py
│   │   │
│   │   ├── database/                      # Работа с БД
│   │   │   ├── __init__.py
│   │   │   ├── models.py                  # SQLAlchemy модели
│   │   │   │
│   │   │   └── repositories/              # Реализации репозиториев
│   │   │       ├── __init__.py
│   │   │       └── report_repository_impl.py  # Impl: ReportRepositoryImpl
│   │   │
│   │   └── external/                      # Внешние сервисы
│   │       └── __init__.py
│   │
│   └── presentation/                      # Presentation Layer (API)
│       ├── __init__.py
│       │
│       ├── api/                           # REST API
│       │   ├── __init__.py
│       │   ├── router.py                  # Главный роутер
│       │   │
│       │   └── v1/                        # API v1
│       │       ├── __init__.py
│       │       │
│       │       ├── endpoints/             # API endpoints
│       │       │   ├── __init__.py
│       │       │   └── reports.py         # Endpoints для отчетов
│       │       │
│       │       └── schemas/               # Pydantic схемы
│       │           ├── __init__.py
│       │           └── report_schema.py   # Схемы валидации
│       │
│       └── middleware/                    # Middleware
│           └── __init__.py
│
├── tests/                                 # Тесты
│   ├── __init__.py
│   ├── unit/                              # Unit тесты
│   │   └── __init__.py
│   └── integration/                       # Integration тесты
│       └── __init__.py
│
├── alembic/                               # Database migrations
│   ├── versions/                          # Файлы миграций
│   │   └── .gitkeep
│   ├── env.py                             # Alembic environment
│   └── script.py.mako                     # Шаблон миграций
│
├── .env                                   # Переменные окружения (локальная)
├── .env.example                           # Пример переменных окружения
├── .gitignore                             # Git ignore правила
├── alembic.ini                            # Конфигурация Alembic
├── docker-compose.yml                     # Docker Compose конфигурация
├── Dockerfile                             # Docker образ приложения
├── requirements.txt                       # Python зависимости
├── README.md                              # Основная документация
├── ARCHITECTURE.md                        # Описание архитектуры
└── PROJECT_STRUCTURE.md                   # Этот файл
```

## Описание основных файлов

### Конфигурация и инфраструктура

- **app/main.py** - Точка входа приложения, инициализация FastAPI
- **app/core/config.py** - Настройки приложения (через Pydantic Settings)
- **app/core/database.py** - Настройка подключения к MySQL, создание engine
- **app/core/dependencies.py** - DI контейнер для всех зависимостей

### Domain Layer (Бизнес-логика)

- **app/domain/entities/report.py** - Сущность Report с бизнес-методами
- **app/domain/repositories/report_repository.py** - Интерфейс репозитория
- **app/domain/services/report_service.py** - Доменный сервис с валидациями

### Application Layer (Use Cases)

- **app/application/dto/report_dto.py** - DTO для передачи данных
- **app/application/use_cases/*** - Реализация бизнес-сценариев

### Infrastructure Layer (Технические детали)

- **app/infrastructure/database/models.py** - SQLAlchemy модели
- **app/infrastructure/database/repositories/*** - Реализация репозиториев

### Presentation Layer (API)

- **app/presentation/api/v1/endpoints/reports.py** - REST API endpoints
- **app/presentation/api/v1/schemas/report_schema.py** - Pydantic схемы
- **app/presentation/api/router.py** - Маршрутизация API

### Конфигурационные файлы

- **requirements.txt** - Все Python зависимости
- **docker-compose.yml** - MySQL + приложение в Docker
- **Dockerfile** - Образ приложения
- **alembic.ini** - Настройки миграций БД
- **.env** - Локальные переменные окружения
- **.gitignore** - Исключения для Git

## Статистика проекта

### Структура слоев

| Слой             | Директория         | Файлов | Назначение                    |
|------------------|-------------------|--------|-------------------------------|
| Domain           | app/domain/       | 3      | Бизнес-логика                 |
| Application      | app/application/  | 6      | Use Cases и DTOs              |
| Infrastructure   | app/infrastructure| 3      | БД и внешние зависимости      |
| Presentation     | app/presentation/ | 3      | REST API                      |
| Core             | app/core/         | 3      | Конфигурация и DI             |

### Технологии

- **Framework**: FastAPI 0.104.1
- **Database**: MySQL 8.0 + SQLAlchemy 2.0
- **Migrations**: Alembic 1.13.0
- **Validation**: Pydantic 2.5.0
- **Testing**: Pytest 7.4.3
- **Async**: aiomysql, asyncio

### Принципы

- ✅ Clean Architecture
- ✅ SOLID principles
- ✅ Dependency Injection
- ✅ Repository Pattern
- ✅ Use Case Pattern
- ✅ DTO Pattern
- ✅ Async/Await
- ✅ Type Hints
- ✅ API Versioning

## Как ориентироваться в проекте

### Для добавления новой фичи:

1. Начните с **Domain Layer** (entities, interfaces)
2. Создайте **Use Case** в Application Layer
3. Реализуйте **Repository** в Infrastructure Layer
4. Добавьте **API endpoint** в Presentation Layer

### Для изменения бизнес-логики:

- Смотрите **app/domain/entities/** и **app/domain/services/**

### Для изменения API:

- Смотрите **app/presentation/api/v1/endpoints/**

### Для изменения работы с БД:

- Смотрите **app/infrastructure/database/**

### Для настройки конфигурации:

- Смотрите **app/core/config.py** и **.env**
