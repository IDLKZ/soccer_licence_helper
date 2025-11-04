"""
Скрипт для проверки подключения к MySQL базе данных
"""
import asyncio
from sqlalchemy import text
from app.core.database import engine
from app.core.config import settings


async def test_connection():
    """Проверить подключение к базе данных"""
    print("=" * 60)
    print("  Проверка подключения к MySQL")
    print("=" * 60)
    print()

    print("Конфигурация подключения:")
    print(f"  Хост: {settings.DB_HOST}")
    print(f"  Порт: {settings.DB_PORT}")
    print(f"  Пользователь: {settings.DB_USER}")
    print(f"  База данных: {settings.DB_NAME}")
    print(f"  URL: {settings.database_url}")
    print()

    print("Попытка подключения...")

    try:
        async with engine.connect() as conn:
            # Проверка подключения
            result = await conn.execute(text("SELECT 1"))
            row = result.fetchone()

            if row and row[0] == 1:
                print("✅ Подключение успешно!")
                print()

                # Получаем версию MySQL
                result = await conn.execute(text("SELECT VERSION()"))
                version = result.fetchone()[0]
                print(f"  MySQL версия: {version}")

                # Получаем текущую базу данных
                result = await conn.execute(text("SELECT DATABASE()"))
                db_name = result.fetchone()[0]
                print(f"  Текущая база: {db_name}")

                # Получаем список таблиц
                result = await conn.execute(text("SHOW TABLES"))
                tables = result.fetchall()

                if tables:
                    print(f"\n  Таблицы в базе ({len(tables)}):")
                    for table in tables:
                        print(f"    - {table[0]}")
                else:
                    print("\n  ⚠️  База данных пустая (нет таблиц)")

                print()
                print("=" * 60)
                print("✅ Тест подключения пройден успешно!")
                print("=" * 60)
                return True
            else:
                print("❌ Неожиданный результат запроса")
                return False

    except Exception as e:
        print(f"❌ Ошибка подключения: {str(e)}")
        print()
        print("Возможные причины:")
        print("  1. MySQL сервер не запущен")
        print("  2. Неправильные учетные данные в .env файле")
        print("  3. База данных не существует")
        print("  4. Нет доступа к базе данных")
        print()
        print("Проверьте настройки в файле .env:")
        print(f"  DB_HOST={settings.DB_HOST}")
        print(f"  DB_PORT={settings.DB_PORT}")
        print(f"  DB_USER={settings.DB_USER}")
        print(f"  DB_PASSWORD=***")
        print(f"  DB_NAME={settings.DB_NAME}")
        print()
        print("=" * 60)
        return False
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_connection())
