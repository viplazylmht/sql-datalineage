with cte1 as (
    select id, name, phone, address from catalog.schema1.customer
    where name like 'join%'
)
, cte2 as (
    select -1 as my_id, 'dummy' as name, 1234 phone, 'unknown' address
)
select * from cte1
union all
select -2 as my_id, 'dummy 2' as name, 12345 phone, 'unknown2' address
union all
select * from cte2
