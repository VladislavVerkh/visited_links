create table visited_domains (
    id serial primary key,
    domain_name  character varying(4000) not null,
    visited_at numeric(30) not null);


create index visited_domains_visited_at_domain_name_i on visited_domains (visited_at, domain_name);