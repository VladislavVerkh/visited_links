import pytest
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST
from fastapi import FastAPI
from httpx import AsyncClient, Response


class TestVisitedLinksRoute:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("visited-links"))
        assert res.status_code != HTTP_404_NOT_FOUND


class TestVisitedLinks:
    @pytest.mark.asyncio
    async def test_if_specified_links_is_not_empty(self, client: AsyncClient) -> None:
        url = "/api/visited_links/"
        data = {
            "links": [
                "https://www.kommersant.ru/doc/6551378?from=top_main_9",
                "https://sportmail.ru/article/betting/60040672/?frommail=1",
            ]
        }
        res: Response = await client.post(url, json=data)

        assert res.text == '{"status":"ok"}'
        assert res.status_code == HTTP_200_OK

    @pytest.mark.asyncio
    async def test_if_specified_links_is_empty(self, client: AsyncClient) -> None:
        url = "/api/visited_links/"
        data = {"links": []}
        res = await client.post(url, json=data)

        assert res.status_code == HTTP_400_BAD_REQUEST
