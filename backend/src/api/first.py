from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(route_class=DishkaRoute)


@router.get("/check-version")  # простой URL
async def greet(session: FromDishka[AsyncSession]) -> str:
    result = await session.execute(text("SELECT version()"))
    version = result.scalar()

    return f"Database version: {version}"


@router.get("/check-users")
async def check_users_table(session: FromDishka[AsyncSession]) -> str:
    # Проверяем, существует ли таблица users
    result = await session.execute(
        text("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'users'
        )
    """)
    )
    table_exists = result.scalar()
    return f"Users table exists: {table_exists}"


@router.get("/db-check")
async def database_check(session: FromDishka[AsyncSession]) -> str:
    try:
        # Простой запрос для проверки подключения
        result = await session.execute(text("SELECT 1"))
        test_result = result.scalar()
        return f"Database connection successful! Test result: {test_result}"
    except Exception as e:
        return f"Database connection failed: {str(e)}"


@router.get("/db-info")
async def database_info(session: FromDishka[AsyncSession]) -> dict:
    # Получаем информацию о БД
    version_result = await session.execute(text("SELECT version()"))
    db_version = version_result.scalar()

    tables_result = await session.execute(
        text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    )
    tables = [row[0] for row in tables_result.fetchall()]

    return {
        "database_version": db_version,
        "tables": tables,
        "message": "Database connection is working!",
    }
