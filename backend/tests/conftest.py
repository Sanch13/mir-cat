import pytest
from httpx import AsyncClient, ASGITransport

from src.main import create_app


@pytest.fixture
def app():
    """Фикстура для создания экземпляра приложения"""
    return create_app()


@pytest.fixture
async def async_client(app):
    """Фикстура для асинхронного клиента"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
