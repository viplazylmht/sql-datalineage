create or replace table latest_customer as
with
cte1 as (
    select id, name, phone from customer where partition = 1
)
, cte2 as (
    select new_id, name, latest_phone from latest_customer where partition = 1
)
select cte1.id, cte1.name, cte2.latest_phone from cte1 cte1
left join cte2 cte2 on cte1.id = cte2.new_id
