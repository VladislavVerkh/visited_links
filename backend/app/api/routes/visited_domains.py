from typing import Annotated
from fastapi import APIRouter, Depends, Body
from fastapi.params import Query
from starlette.status import HTTP_200_OK
from app.api.dependencies.database import get_repository
from app.models.visited_link import GetVisitedDomainsResponse
from app.db.repositories.visited_domain_repository import VisitedDomainRepository

router = APIRouter(prefix="/visited_domains", tags=["domains"])


def validate_period(from_time: int, to_time: int):
    if from_time and to_time and from_time > to_time:
        raise ValueError("Дата окончания должна быть не меньше чем дата начала периода")


@router.get(
    "/",
    description="Возвращает полный список доменов, посещенных работником",
    summary="Find all visited domains",
    name="visited-domains",
    status_code=HTTP_200_OK,
)
async def find_visited_domains(
    visited_domain_repository: VisitedDomainRepository = Depends(
        get_repository(VisitedDomainRepository)
    ),
    from_time: Annotated[
        int | None,
        Query(
            alias="from",
            description="С какого времени в формате (число секунд с начала эпохи)",
        ),
    ] = None,
    to_time: Annotated[
        int | None,
        Query(
            alias="to",
            description="По какое время в формате (число секунд с начала эпохи)",
        ),
    ] = None,
) -> GetVisitedDomainsResponse:
    validate_period(from_time=from_time, to_time=to_time)
    visited_domains = await visited_domain_repository.find_visited_domains(
        from_time, to_time
    )
    return GetVisitedDomainsResponse(domains=visited_domains)
