merge into catalog.schema1.customer_metric c
using (
select c.name, c.phone, null as address, coalesce(mb.state, 'default') as state
from catalog.schema1.customer c 
left join catalog.schema1.metric_basis mb on c.address = mb.address
) d
on c.name = d.name
when matched then update set state = COALESCE(c.state, d.state), phone = d.phone
when not matched by source then update set address = COALESCE(c.address, 'default')
when not matched then insert
values(d.name, d.phone, d.address, d.state, 'unknown')
