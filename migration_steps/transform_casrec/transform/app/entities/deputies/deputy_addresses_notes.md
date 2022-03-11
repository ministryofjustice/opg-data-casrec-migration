SQL equivalent:

```sql
with addresses_df as (
    select *
    from {config.schemas["pre_transform"]}.deputy_address
),

deputyship_df as (
    select distinct "Dep Addr No", "Deputy No"
    from {config.schemas["pre_transform"]}.deputyship
),

persons_df as (
    select id as personid, c_deputy_no
    from etl2.persons
    where type = 'actor_deputy'
)


select *
from addresses_df
inner join deputyship_df on deputyship_df."Dep Addr No" = addresses_df."Dep Addr No"
inner join persons_df on deputyship_df."Deputy No" = persons_df.c_deputy_no
```
