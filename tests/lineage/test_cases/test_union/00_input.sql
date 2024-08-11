with
cte1 as (
    select id, name, phone from customer where partition = 1
)
, cte2 as (
    select new_id, name, latest_phone from latest_customer where partition = 1
)
select * from cte1
union all
select * from cte2
union all
select * from cte2
