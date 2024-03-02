from typing import List, Optional
from app.db.repositories.base_repository import BaseRepository

from app.models.visited_link import VisitedDomainEntity


class VisitedDomainRepository(BaseRepository):
    async def find_visited_domains(
        self, from_time: Optional[int] = None, to_time: Optional[int] = None
    ) -> list[str]:
        values = dict(from_time=from_time, to_time=to_time)
        visited_domains = await self.db.fetch_all(
            query=self.SQL.SELECT_VISITED_DOMAINS, values=values
        )
        return sorted([row["domain_name"] for row in visited_domains])

    async def save_visited_domains(
        self, visited_domains_entities: List[VisitedDomainEntity]
    ):
        values = [dict(domain) for domain in visited_domains_entities]
        visited_links = await self.db.execute_many(
            query=self.SQL.INSERT_VISITED_DOMAIN, values=values
        )

        return visited_links

    class SQL:
        SELECT_VISITED_DOMAINS = """
            select distinct domain_name as domain_name
              from visited_domains
             where visited_at >= coalesce(:from_time,visited_at)
               and visited_at <= coalesce(:to_time, visited_at);
        """

        INSERT_VISITED_DOMAIN = """
            insert into visited_domains (domain_name, visited_at)
            values (:domain_name, :visited_at);
        """
