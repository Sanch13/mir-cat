import pytest
import asyncio


# Синхронный тест - работает без пометок
def test_sync():
    assert 2 * 2 == 4


# Асинхронный тест - требует @pytest.mark.asyncio
@pytest.mark.asyncio
async def test_async():
    await asyncio.sleep(0.1)
    assert 3 + 3 == 6


# Асинхронный тест с клиентом FastAPI
@pytest.mark.asyncio
async def test_health_check(async_client):
    """Тест эндпоинта"""
    response = await async_client.get("/api/v1/hello")
    assert response.status_code == 200
