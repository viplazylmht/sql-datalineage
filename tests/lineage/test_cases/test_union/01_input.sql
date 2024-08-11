with
cte1 as (
    select id, name, phone from customer where partition = 1
)
, cte2 as (
    select new_id, name, latest_phone from latest_customer where partition = 1
)
, static_data as (
    select 1 as new_id, 'DUMMY' name, 143215 as latest_phone
    from customer
)
select * from cte1
union all
select * from static_data
union all
select * from cte2
