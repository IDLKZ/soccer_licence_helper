"""Check application_steps table schema"""
import asyncio
from sqlalchemy import text
from app.core.database import engine

async def check_schema():
    async with engine.begin() as conn:
        result = await conn.execute(text("DESCRIBE application_steps"))
        print("application_steps table structure:")
        for row in result:
            print(f"  {row[0]}: {row[1]}")

asyncio.run(check_schema())
