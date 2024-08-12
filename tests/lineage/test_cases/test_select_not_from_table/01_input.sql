with cte1 as (
    select id, name, phone, address from catalog.schema1.customer
    where name like 'join%'
)
, cte2 as (
    select d.* from (
        select -1 as my_id, 'dummy' as name, 1234 phone, 'unknown' address
    ) d
)
select * from cte1
union all
select * from cte2
