from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(route_class=DishkaRoute)


@router.get("/hello")  # простой URL
async def greet(session: FromDishka[AsyncSession]) -> str:
    return "Answer: Good morning AXAXAAX"


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
