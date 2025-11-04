# Report Generation Microservice

Микросервис для генерации отчетов по лицензированию футбольных клубов на основе Clean Architecture.

## Возможности

- ✅ Генерация PDF отчетов по заявкам клубов
- ✅ Clean Architecture (Domain, Application, Infrastructure, Presentation слои)
- ✅ Асинхронная работа с базой данных (SQLAlchemy 2.0 + aiomysql)
- ✅ Единственный endpoint: `POST /api/v1/reports/generate`
- ✅ Рендеринг HTML шаблонов через Jinja2
- ✅ Конвертация HTML → PDF через pdfkit/wkhtmltopdf

## Требования

1. **Python 3.10+**
2. **MySQL 8.0+** (существующая база данных)
3. **wkhtmltopdf**
   - Windows: Скачайте с https://wkhtmltopdf.org/ и установите в `C:\Program Files\wkhtmltopdf\`
   - Linux: `apt-get install wkhtmltopdf` или `yum install wkhtmltopdf`

## Установка

### 1. Клонируйте репозиторий

```bash
cd license_helper
```

### 2. Создайте виртуальное окружение

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Настройте .env файл

Создайте файл `.env` в корне проекта:

```env
# Database
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_NAME=your_database_name

# Application
APP_NAME=Report Generation Service
APP_VERSION=1.0.0
APP_ENV=development
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### 5. Поместите шаблон и логотип

- Шаблон отчета: `templates/report_template.html` ✅ (уже добавлен)
- Логотип: `templates/logo_white.png` (добавьте PNG файл)

## Запуск

### Development режим

```bash
python -m app.main
```

Или:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production режим

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Использование API

### Endpoint

```
POST http://localhost:8000/api/v1/reports/generate
```

### Request Body

```json
{
  "report_id": 1
}
```

### Response

PDF файл с именем `report_{report_id}.pdf`

### Пример с curl

```bash
curl -X POST "http://localhost:8000/api/v1/reports/generate" \
  -H "Content-Type: application/json" \
  -d '{"report_id": 1}' \
  --output report.pdf
```

### Пример с Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/reports/generate",
    json={"report_id": 1}
)

if response.status_code == 200:
    with open("report.pdf", "wb") as f:
        f.write(response.content)
    print("Отчет сохранен в report.pdf")
else:
    print(f"Ошибка: {response.status_code}")
    print(response.json())
```

## Документация API

После запуска сервиса:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

## Структура проекта

```
license_helper/
├── app/
│   ├── domain/              # Бизнес-логика (entities, интерфейсы)
│   │   ├── entities/
│   │   ├── repositories/
│   │   └── services/
│   ├── application/         # Use Cases и DTOs
│   │   ├── dto/
│   │   └── use_cases/
│   ├── infrastructure/      # Реализации (DB, services)
│   │   ├── database/
│   │   │   └── models/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── mappers/
│   ├── presentation/        # API layer
│   │   └── api/
│   │       └── v1/
│   │           ├── routers/
│   │           └── schemas/
│   ├── core/                # Конфигурация
│   └── main.py              # Точка входа
├── templates/               # HTML шаблоны
│   ├── report_template.html
│   └── logo_white.png
├── .env                     # Переменные окружения
├── requirements.txt
└── README_REPORT_SERVICE.md
```

## Архитектура

Проект следует принципам **Clean Architecture**:

1. **Domain Layer** - Чистая бизнес-логика
   - Entities (ApplicationReport, ApplicationCriteria, Club, License и др.)
   - Интерфейсы репозиториев и сервисов

2. **Application Layer** - Use Cases
   - `GenerateReportUseCaseV2` - генерация данных отчета
   - DTOs для передачи данных между слоями

3. **Infrastructure Layer** - Внешние зависимости
   - SQLAlchemy модели и репозитории
   - Сервисы рендеринга (Jinja2) и генерации PDF (pdfkit)

4. **Presentation Layer** - API
   - FastAPI роутеры и эндпоинты
   - Dependency Injection

## Бизнес-логика генерации отчета

1. Получение отчета из базы по `report_id`
2. Загрузка всех связанных данных (criteria, application, club, license, season, documents)
3. Группировка документов по `document_id` в статьи
4. Фильтрация документов в зависимости от `report.status`:
   - `status = 0` - все документы
   - `status = 1` - только принятые документы
5. Генерация итогового текста (summary):
   - Все приняты → "все документы соответствуют"
   - Все отклонены → "все документы отклонены"
   - Смешанный → "некоторые документы не соответствуют"
6. Рендеринг HTML шаблона с данными
7. Конвертация HTML → PDF через wkhtmltopdf
8. Возврат PDF через FileResponse

## Troubleshooting

### Ошибка: wkhtmltopdf not found

**Windows:**
```
Скачайте и установите wkhtmltopdf в C:\Program Files\wkhtmltopdf\
```

**Linux:**
```bash
sudo apt-get install wkhtmltopdf
```

### Ошибка: Template not found

Убедитесь что файл `templates/report_template.html` существует.

### Ошибка: Database connection failed

Проверьте настройки в `.env` файле и доступность базы данных.

### Ошибка: Logo not found

Если логотип не найден, отчет сгенерируется с пустым logo_base64.
Добавьте файл `templates/logo_white.png`.

## Docker (опционально)

Запуск через Docker Compose:

```bash
docker-compose up -d
```

## Разработка

### Установка dev зависимостей

```bash
pip install -r requirements.txt
```

### Тестирование

```bash
pytest
```

### Линтинг

```bash
black app/
flake8 app/
mypy app/
```

## Лицензия

MIT

## Контакты

Если возникли вопросы, создайте issue в репозитории.
