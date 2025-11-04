# Настройка подключения к MySQL

## 📋 Конфигурация уже готова!

Подключение к MySQL уже настроено через `.env` файл. Все параметры БД находятся там.

## ⚙️ Текущие настройки (.env)

```env
# Database
DB_HOST=localhost          # Хост MySQL сервера
DB_PORT=3306              # Порт MySQL (по умолчанию 3306)
DB_USER=root              # Пользователь БД
DB_PASSWORD=rootpassword  # Пароль
DB_NAME=license_helper    # Название базы данных
DB_POOL_SIZE=10           # Размер пула подключений
DB_MAX_OVERFLOW=20        # Максимальное переполнение пула
```

## 🔧 Как изменить настройки

1. Откройте файл `.env` в корне проекта
2. Измените нужные параметры:

```env
DB_HOST=localhost              # ← Измените хост если БД на другом сервере
DB_PORT=3306                   # ← Измените порт если используется другой
DB_USER=ваш_пользователь       # ← Ваш пользователь MySQL
DB_PASSWORD=ваш_пароль         # ← Ваш пароль
DB_NAME=ваша_база_данных       # ← Название вашей существующей БД
```

3. Сохраните файл

## 🚀 Проверка подключения

После настройки `.env` файла, проверьте подключение:

```bash
python test_db_connection.py
```

Вы должны увидеть:
```
✅ Подключение успешно!
  MySQL версия: 8.0.x
  Текущая база: license_helper
  Таблицы в базе (13):
    - users
    - clubs
    - club_types
    - ...
```

## ❗ Важно

### Это микросервис НЕ создает таблицы!

Микросервис подключается к **СУЩЕСТВУЮЩЕЙ** базе данных с таблицами:
- `users`
- `clubs`
- `club_types`
- `category_documents`
- `seasons`
- `leagues`
- `licenses`
- `applications`
- `application_criteria`
- `documents`
- `application_documents`
- `application_reports`

### База данных должна уже существовать!

Если база данных пустая или таблицы не созданы, микросервис НЕ будет работать.

## 🔍 Как работает подключение

### app/core/config.py
Читает параметры из `.env`:
```python
class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "license_helper"

    @property
    def database_url(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
```

### app/core/database.py
Создает async engine для подключения:
```python
engine = create_async_engine(
    settings.database_url,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True  # ← Проверка подключения перед использованием
)
```

## 🐛 Troubleshooting

### Ошибка: Access denied for user

```
❌ Access denied for user 'root'@'localhost'
```

**Решение:**
1. Проверьте `DB_USER` и `DB_PASSWORD` в `.env`
2. Убедитесь что пользователь существует в MySQL
3. Проверьте права доступа:
```sql
GRANT ALL PRIVILEGES ON license_helper.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### Ошибка: Unknown database

```
❌ Unknown database 'license_helper'
```

**Решение:**
1. Создайте базу данных:
```sql
CREATE DATABASE license_helper CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Или измените `DB_NAME` в `.env` на существующую базу

### Ошибка: Can't connect to MySQL server

```
❌ Can't connect to MySQL server on 'localhost'
```

**Решение:**
1. Убедитесь что MySQL сервер запущен:
```bash
# Windows
net start MySQL80

# Linux
sudo systemctl start mysql
```

2. Проверьте порт:
```bash
netstat -an | grep 3306
```

### Ошибка: No module named 'aiomysql'

```
❌ No module named 'aiomysql'
```

**Решение:**
```bash
pip install -r requirements.txt
```

## 📊 Используемые драйверы

- **Асинхронный**: `aiomysql` (для FastAPI endpoints)
- **Синхронный**: `pymysql` (для Alembic миграций, если нужно)

Оба уже указаны в `requirements.txt`:
```txt
aiomysql==0.2.0
pymysql==1.1.0
cryptography==41.0.7  # Требуется для MySQL
```

## 🔒 Безопасность

### Продакшн

Для продакшна используйте:
1. Отдельного пользователя БД (не root)
2. Сильный пароль
3. Ограниченные права доступа
4. SSL соединение (опционально)

Пример:
```sql
CREATE USER 'license_app'@'%' IDENTIFIED BY 'strong_password_here';
GRANT SELECT, INSERT, UPDATE ON license_helper.* TO 'license_app'@'%';
FLUSH PRIVILEGES;
```

В `.env`:
```env
DB_USER=license_app
DB_PASSWORD=strong_password_here
```

### Не коммитьте .env в git!

Файл `.env` уже добавлен в `.gitignore`.

## ✅ Готово!

После настройки `.env` просто запускайте:
```bash
python -m app.main
```

Приложение автоматически подключится к MySQL используя параметры из `.env`.
