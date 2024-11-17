merge into catalog.schema1.customer_metric c
using catalog.schema1.customer d
on c.name = d.name
when matched then update set state = COALESCE(c.state, d.state), phone = d.phone
when not matched then insert
values(d.name, d.phone, d.address, 'no state', 'unknown')
