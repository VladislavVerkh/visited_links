import pytest
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST
from fastapi import FastAPI
from httpx import AsyncClient

from app.db.repositories.visited_domain_repository import VisitedDomainRepository


class TestVisitedDomainsRoute:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(app.url_path_for("visited-domains"))
        assert res.status_code != HTTP_404_NOT_FOUND


class TestVisitedDomains:
    async def prepare_data(self, app: FastAPI):
        await app.state._db.execute(query="truncate table visited_domains")

        values = [
            {"domain_name": "mail.ru", "visited_at": 1709335700},
            {"domain_name": "ya.ru", "visited_at": 1709335718},
            {"domain_name": "mail.ru", "visited_at": 1709335719},
            {"domain_name": "avito.ru", "visited_at": 1709335729},
            {"domain_name": "sber.ru", "visited_at": 1709335729},
            {"domain_name": "sber.ru", "visited_at": 1709335729},
        ]

        await app.state._db.execute_many(
            query=VisitedDomainRepository.SQL.INSERT_VISITED_DOMAIN, values=values
        )

    @pytest.mark.asyncio
    async def test_if_specified_from_time(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        await self.prepare_data(app)

        url = "/api/visited_domains/?from=1709335729"
        res = await client.get(url)
        assert res.status_code == HTTP_200_OK
        assert res.text == '{"domains":["avito.ru","sber.ru"],"status":"ok"}'

    @pytest.mark.asyncio
    async def test_if_specified_to_time(self, client: AsyncClient) -> None:
        url = "/api/visited_domains/?to=1709335718"
        res = await client.get(url)
        assert res.status_code == HTTP_200_OK
        assert res.text == '{"domains":["mail.ru","ya.ru"],"status":"ok"}'

    @pytest.mark.asyncio
    async def test_if_specified_from_time_and_to_time_is_correct(
        self, client: AsyncClient
    ) -> None:
        url = "/api/visited_domains/?from=1709335719&to=1709335720"
        res = await client.get(url)
        assert res.status_code == HTTP_200_OK

    @pytest.mark.asyncio
    async def test_if_specified_from_time_and_to_time_is_wrong(
        self, client: AsyncClient
    ) -> None:
        url = "/api/visited_domains/?from=1709335730&to=1709335711"
        res = await client.get(url)
        assert res.status_code == HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_if_not_specified_from_and_to(self, client: AsyncClient) -> None:
        url = "/api/visited_domains/"
        res = await client.get(url)
        assert res.status_code == HTTP_200_OK
        assert (
            res.text
            == '{"domains":["avito.ru","mail.ru","sber.ru","ya.ru"],"status":"ok"}'
        )
