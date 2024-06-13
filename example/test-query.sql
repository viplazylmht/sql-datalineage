with cte1 as (
    select id, name, phone, address from catalog.schema1.customer
    where name like 'duy%'
)
, tmp_cte as (
select id, name, age, phone, customer_job from catalog.schema1.user_demographics
)
, cte2 as (
select id, name, age, phone, customer_job job from tmp_cte
)
, cte3 as (
select id, name, age, phone, job from catalog.schema1.tbl_cte3
)
select * from (
select t1.*, concat(t1.name, t2.name) as full_name, max(age) as max_age
from cte1 t1 left join cte2 t2 on t1.phone = t2.phone
group by t1.id, concat(t1.name, t2.name)
having max(age) > 10
) where id < 5
