import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database
import pytest_asyncio


@pytest_asyncio.fixture
def app() -> FastAPI:
    from app.api.server import get_application

    return get_application()


@pytest_asyncio.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://localhost:8000",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client
