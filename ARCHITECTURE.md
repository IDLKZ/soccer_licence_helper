# Архитектура License Helper Service

## Обзор

License Helper Service построен по принципам **Clean Architecture** с четким разделением ответственности и зависимостей между слоями.

## Принципы Clean Architecture

1. **Независимость от фреймворков** - Бизнес-логика не зависит от FastAPI или других внешних библиотек
2. **Тестируемость** - Бизнес-логика может быть протестирована без UI, БД и внешних сервисов
3. **Независимость от UI** - API можно заменить на CLI, gRPC и т.д. без изменения бизнес-логики
4. **Независимость от БД** - MySQL можно заменить на PostgreSQL, MongoDB и т.д.
5. **Правило зависимостей** - Зависимости направлены только внутрь (к Domain)

## Структура слоев

```
┌─────────────────────────────────────────────┐
│         Presentation Layer (API)            │  ← Внешний слой
│  - REST API endpoints                       │
│  - Pydantic schemas                         │
│  - Request/Response models                  │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         Application Layer                   │  ← Use Cases
│  - Use Cases (бизнес-сценарии)              │
│  - DTOs (Data Transfer Objects)             │
│  - Orchestration logic                      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         Domain Layer                        │  ← Ядро системы
│  - Entities (бизнес-сущности)               │
│  - Repository Interfaces                    │
│  - Domain Services                          │
│  - Business Rules                           │
└─────────────────────────────────────────────┘
                    ↑
┌─────────────────────────────────────────────┐
│         Infrastructure Layer                │  ← Внешние зависимости
│  - Database (SQLAlchemy)                    │
│  - Repository Implementations               │
│  - External Services                        │
│  - Configuration                            │
└─────────────────────────────────────────────┘
```

## Детальное описание слоев

### 1. Domain Layer (`app/domain/`)

**Назначение**: Ядро бизнес-логики приложения

**Компоненты**:
- **Entities** (`entities/report.py`)
  - Чистые бизнес-сущности без зависимостей
  - `Report` - основная сущность отчета
  - Содержит бизнес-методы (`mark_as_completed`, `mark_as_failed`, и т.д.)
  - Enum'ы: `ReportStatus`, `ReportType`

- **Repository Interfaces** (`repositories/report_repository.py`)
  - Абстрактные интерфейсы для работы с данными
  - `IReportRepository` - контракт для репозитория
  - Определяет методы: `create`, `get_by_id`, `get_all`, `update`, `delete`, `count`

- **Domain Services** (`services/report_service.py`)
  - `ReportDomainService` - бизнес-правила и валидации
  - Валидация параметров отчетов
  - Расчет приоритетов
  - Генерация имен файлов

**Правила**:
- Не зависит от других слоев
- Не содержит ссылок на фреймворки (FastAPI, SQLAlchemy)
- Содержит только чистую бизнес-логику

### 2. Application Layer (`app/application/`)

**Назначение**: Реализация сценариев использования

**Компоненты**:
- **DTOs** (`dto/report_dto.py`)
  - `CreateReportDTO` - для создания отчета
  - `ReportDTO` - для отображения отчета
  - `ReportListDTO` - для списка с пагинацией
  - `GenerateReportResultDTO` - результат генерации

- **Use Cases** (`use_cases/`)
  - `CreateReportUseCase` - создание нового отчета
  - `GenerateReportUseCase` - генерация отчета
  - `GetReportUseCase` - получение отчета по ID
  - `ListReportsUseCase` - получение списка с фильтрацией
  - `DeleteReportUseCase` - удаление отчета

**Правила**:
- Зависит только от Domain Layer
- Координирует выполнение бизнес-логики
- Не содержит деталей реализации (БД, API)

### 3. Infrastructure Layer (`app/infrastructure/`)

**Назначение**: Реализация технических деталей и внешних зависимостей

**Компоненты**:
- **Database Models** (`database/models.py`)
  - `ReportModel` - SQLAlchemy модель для БД
  - Маппинг на таблицу `reports`

- **Repository Implementations** (`database/repositories/`)
  - `ReportRepositoryImpl` - реализация `IReportRepository`
  - Использует SQLAlchemy для работы с MySQL
  - Конвертирует между моделями БД и доменными сущностями

- **Core** (`app/core/`)
  - `config.py` - конфигурация через Pydantic Settings
  - `database.py` - настройка подключения к БД
  - `dependencies.py` - Dependency Injection

**Правила**:
- Зависит от Domain Layer (использует интерфейсы)
- Содержит детали реализации (SQLAlchemy, MySQL)
- Может быть заменен без изменения бизнес-логики

### 4. Presentation Layer (`app/presentation/`)

**Назначение**: API для взаимодействия с клиентами

**Компоненты**:
- **API Endpoints** (`api/v1/endpoints/reports.py`)
  - `POST /api/v1/reports/` - создание отчета
  - `GET /api/v1/reports/` - список отчетов
  - `GET /api/v1/reports/{id}` - получение отчета
  - `POST /api/v1/reports/{id}/generate` - генерация
  - `DELETE /api/v1/reports/{id}` - удаление
  - `GET /api/v1/reports/{id}/download` - скачивание

- **Schemas** (`api/v1/schemas/report_schema.py`)
  - Pydantic модели для валидации запросов/ответов
  - `ReportCreateRequest`, `ReportResponse`, и т.д.

- **Router** (`api/router.py`)
  - Настройка маршрутизации
  - Версионирование API (v1, v2, ...)

**Правила**:
- Зависит от Application Layer (использует Use Cases)
- Не содержит бизнес-логики
- Только адаптация запросов/ответов

## Поток данных

### Пример: Создание отчета

```
1. Client → POST /api/v1/reports/ (JSON)
                ↓
2. Presentation Layer
   - reports.py:create_report()
   - Валидация через ReportCreateRequest (Pydantic)
                ↓
3. Application Layer
   - CreateReportUseCase.execute()
   - Конвертация в CreateReportDTO
   - Валидация через ReportDomainService
                ↓
4. Domain Layer
   - Создание entity Report
   - Бизнес-правила и валидации
                ↓
5. Infrastructure Layer
   - ReportRepositoryImpl.create()
   - Сохранение в MySQL через SQLAlchemy
                ↓
6. Response ← ReportDTO ← Domain Entity
```

## Dependency Injection

Все зависимости инжектируются через `app/core/dependencies.py`:

```python
# Пример
get_create_report_use_case(
    repository = IReportRepository,  # Интерфейс
    service = ReportDomainService
) → CreateReportUseCase
```

**Преимущества**:
- Легко заменить реализацию (например, MockRepository для тестов)
- Инверсия зависимостей (Domain не знает об Infrastructure)
- Легко добавлять новые зависимости

## База данных

### Миграции (Alembic)

```bash
# Создать миграцию
alembic revision --autogenerate -m "Initial migration"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1
```

### Модель данных

**Таблица: reports**

| Колонка        | Тип           | Описание                    |
|----------------|---------------|-----------------------------|
| id             | INT           | Primary key                 |
| name           | VARCHAR(255)  | Название отчета             |
| report_type    | ENUM          | Тип отчета                  |
| status         | ENUM          | Статус (pending/processing) |
| parameters     | JSON          | Параметры генерации         |
| file_path      | VARCHAR(500)  | Путь к файлу                |
| error_message  | TEXT          | Сообщение об ошибке         |
| created_at     | DATETIME      | Дата создания               |
| updated_at     | DATETIME      | Дата обновления             |
| completed_at   | DATETIME      | Дата завершения             |

## Расширение функциональности

### Добавление нового типа отчета

1. Добавить в `ReportType` enum (`domain/entities/report.py`)
2. Добавить валидацию в `ReportDomainService`
3. Реализовать генератор отчета
4. Обновить документацию API

### Добавление новой сущности

1. Создать entity в `domain/entities/`
2. Создать repository interface в `domain/repositories/`
3. Создать SQLAlchemy модель в `infrastructure/database/models.py`
4. Реализовать repository в `infrastructure/database/repositories/`
5. Создать Use Cases в `application/use_cases/`
6. Создать API endpoints в `presentation/api/v1/endpoints/`

### Замена БД

1. Создать новую реализацию `IReportRepository`
2. Обновить `dependencies.py` для использования новой реализации
3. Бизнес-логика остается без изменений!

## Тестирование

### Unit тесты (Domain Layer)

```python
# tests/unit/test_report_entity.py
def test_mark_as_completed():
    report = Report(name="Test", report_type=ReportType.LICENSE_SUMMARY)
    report.mark_as_completed("/path/to/file.pdf")
    assert report.status == ReportStatus.COMPLETED
```

### Integration тесты (Application Layer)

```python
# tests/integration/test_create_report_use_case.py
async def test_create_report_use_case():
    mock_repo = MockReportRepository()
    use_case = CreateReportUseCase(mock_repo, ReportDomainService())
    result = await use_case.execute(dto)
    assert result.id is not None
```

### API тесты (Presentation Layer)

```python
# tests/integration/test_api.py
async def test_create_report_endpoint(client):
    response = await client.post("/api/v1/reports/", json=payload)
    assert response.status_code == 201
```

## Безопасность

### Текущие меры

- Валидация входных данных через Pydantic
- Параметризованные SQL запросы (SQLAlchemy)
- CORS middleware

### TODO

- [ ] Аутентификация (JWT tokens)
- [ ] Авторизация (role-based access)
- [ ] Rate limiting
- [ ] Input sanitization для file paths
- [ ] Шифрование чувствительных данных

## Производительность

### Оптимизации

- Асинхронная работа с БД (aiomysql)
- Connection pooling (настроено в config)
- Пагинация для списков
- Индексы на частые запросы (status, report_type)

### Мониторинг

- TODO: Добавить метрики (Prometheus)
- TODO: Логирование (структурированное)
- TODO: Трейсинг (OpenTelemetry)

## Развертывание

### Docker

```bash
# Запуск всего стека
docker-compose up -d

# Только MySQL
docker-compose up -d mysql

# Только приложение
docker-compose up -d app
```

### Локальная разработка

```bash
# 1. Установка зависимостей
pip install -r requirements.txt

# 2. Настройка .env
cp .env.example .env

# 3. Запуск БД
docker-compose up -d mysql

# 4. Миграции
alembic upgrade head

# 5. Запуск приложения
uvicorn app.main:app --reload
```

## Следующие шаги

1. **Реализовать реальную генерацию отчетов**
   - PDF генератор (ReportLab, WeasyPrint)
   - Excel генератор (openpyxl)
   - CSV генератор

2. **Добавить фоновую обработку**
   - Celery для асинхронной генерации
   - Redis для очередей

3. **Расширить доменную модель**
   - Добавить сущности: License, Product, User
   - Связи между сущностями

4. **Улучшить API**
   - Аутентификация и авторизация
   - Websockets для уведомлений о статусе
   - Swagger UI кастомизация

5. **Тестирование**
   - Unit тесты для всех слоев
   - Integration тесты
   - E2E тесты

6. **Мониторинг и логирование**
   - Структурированное логирование
   - Метрики для Prometheus
   - Distributed tracing
