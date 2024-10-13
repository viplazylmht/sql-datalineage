insert into latest_customer(location, address, name, latest_phone, new_id)
with
cte1 as (
    select id, name, phone, location, address from customer where partition = 1
)
, cte2 as (
    select new_id, name, latest_phone from latest_customer where partition = 1
)
select cte1.location, cte1.address, cte2.name, cte1.phone, cte1.id from cte1 cte1
left join cte2 cte2 on cte1.id = cte2.new_id
