from pydantic import BaseModel


class VisitedDomainEntity(BaseModel):
    domain_name: str
    visited_at: int


class CreateVisitedLinkRequest(BaseModel):
    links: list[str]


class CreateVisitedLinkResponse(BaseModel):
    status: str = "ok"


class GetVisitedDomainsResponse(BaseModel):
    domains: list[str]
    status: str = "ok"
