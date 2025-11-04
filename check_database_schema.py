"""
Скрипт для проверки схемы таблиц в БД
Показывает реальные колонки для каждой таблицы
"""
import asyncio
from sqlalchemy import text, inspect
from app.core.database import engine
from app.core.config import settings


async def check_schema():
    """Проверить схему всех таблиц"""
    print("=" * 80)
    print("  Проверка схемы базы данных")
    print("=" * 80)
    print()

    tables_to_check = [
        "users",
        "clubs",
        "club_types",
        "category_documents",
        "seasons",
        "leagues",
        "licenses",
        "applications",
        "application_criteria",
        "documents",
        "application_documents",
        "application_reports",
    ]

    try:
        async with engine.connect() as conn:
            for table_name in tables_to_check:
                print(f"\nTable: {table_name}")
                print("-" * 80)

                # Получаем описание колонок
                result = await conn.execute(text(f"DESCRIBE {table_name}"))
                columns = result.fetchall()

                if columns:
                    print(f"{'Field':<30} {'Type':<25} {'Null':<6} {'Key':<6} {'Default':<15}")
                    print("-" * 80)
                    for col in columns:
                        field = col[0]
                        col_type = col[1]
                        null = col[2]
                        key = col[3]
                        default = col[4] if col[4] is not None else "NULL"
                        print(f"{field:<30} {col_type:<25} {null:<6} {key:<6} {default:<15}")
                else:
                    print(f"WARNING: Table is empty or does not exist")

            print()
            print("=" * 80)
            print("Schema check completed")
            print("=" * 80)

    except Exception as e:
        print(f"ERROR: {str(e)}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(check_schema())
