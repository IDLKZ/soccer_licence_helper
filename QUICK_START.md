# 🚀 Быстрый старт - Report Generation Service

## Шаг 1: Настройте подключение к MySQL

### Откройте файл `.env` и укажите параметры вашей БД:

```env
# Database - ИЗМЕНИТЕ ЭТИ ПАРАМЕТРЫ!
DB_HOST=localhost              # ← Хост вашего MySQL сервера
DB_PORT=3306                   # ← Порт (обычно 3306)
DB_USER=root                   # ← Ваш пользователь MySQL
DB_PASSWORD=rootpassword       # ← Ваш пароль MySQL
DB_NAME=license_helper         # ← Название вашей существующей базы данных
```

**⚠️ ВАЖНО:** База данных должна **УЖЕ СУЩЕСТВОВАТЬ** со всеми таблицами!

Нужные таблицы:
- users
- clubs
- club_types
- category_documents
- seasons
- leagues
- licenses
- applications
- application_criteria
- documents
- application_documents
- application_reports

## Шаг 2: Проверьте подключение к БД

```bash
python test_db_connection.py
```

Должны увидеть:
```
✅ Подключение успешно!
  MySQL версия: 8.0.x
  Текущая база: license_helper
  Таблицы в базе (13):
    - users
    - clubs
    ...
```

## Шаг 3: Установите wkhtmltopdf

### Windows:
1. Скачайте: https://wkhtmltopdf.org/downloads.html
2. Установите в `C:\Program Files\wkhtmltopdf\`

### Linux:
```bash
sudo apt-get install wkhtmltopdf
```

## Шаг 4: Добавьте логотип

Поместите PNG файл в:
```
templates/logo_white.png
```

(Опционально - если логотипа нет, отчет сгенерируется без него)

## Шаг 5: Установите зависимости

```bash
pip install -r requirements.txt
```

## Шаг 6: Запустите сервер

```bash
python -m app.main
```

Вы должны увидеть:
```
Starting up...
Connecting to existing database...
Ready to use existing database
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Шаг 7: Протестируйте API

### Откройте документацию:
```
http://localhost:8000/api/docs
```

### Или используйте тестовый скрипт:
```bash
python test_generate_report.py 1
```

### Или curl:
```bash
curl -X POST "http://localhost:8000/api/v1/reports/generate" \
  -H "Content-Type: application/json" \
  -d '{"report_id": 1}' \
  --output report.pdf
```

## ✅ Готово!

Если всё прошло успешно, вы получите PDF файл с отчетом!

---

## 📚 Дополнительная документация

- `MYSQL_SETUP.md` - Подробная настройка MySQL
- `README_REPORT_SERVICE.md` - Полная документация сервиса
- `.env.example` - Пример конфигурации

## ❓ Проблемы?

### Ошибка подключения к БД:
```bash
python test_db_connection.py
```
Проверьте параметры в `.env`

### Ошибка "Template not found":
Убедитесь что существует `templates/report_template.html`

### Ошибка "wkhtmltopdf not found":
Установите wkhtmltopdf (см. Шаг 3)

---

**Всё должно работать! 🎉**
