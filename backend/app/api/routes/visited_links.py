import datetime
import time
from typing import Annotated
from fastapi import APIRouter, Depends, Body
from starlette.status import HTTP_200_OK
from app.api.dependencies.database import get_repository
from app.models.visited_link import CreateVisitedLinkRequest
from urllib.parse import urlparse
from app.models.visited_link import CreateVisitedLinkResponse
from app.db.repositories.visited_domain_repository import VisitedDomainRepository
from app.models.visited_link import VisitedDomainEntity

router = APIRouter(
    prefix="/visited_links",
    tags=["links"],
)


def validate_links(links: list[str]):
    if not links or len(links) == 0:
        raise ValueError("Не указан список ссылок")


@router.post(
    "/",
    description="Принимает список ссылок, которые были посещены работником",
    summary="Save visited links",
    name="visited-links",
    status_code=HTTP_200_OK,
)
async def save_visited_links(
    links: Annotated[CreateVisitedLinkRequest, Body(embed=False)],
    visited_domain_repository: VisitedDomainRepository = Depends(
        get_repository(VisitedDomainRepository)
    ),
) -> CreateVisitedLinkResponse:
    validate_links(links.links)

    visited_at_unix = int(time.mktime(datetime.datetime.now().timetuple()))

    visited_domain_entities = [
        VisitedDomainEntity(
            link=link, domain_name=urlparse(link).netloc, visited_at=visited_at_unix
        )
        for link in links.links
    ]

    await visited_domain_repository.save_visited_domains(visited_domain_entities)

    return CreateVisitedLinkResponse()
