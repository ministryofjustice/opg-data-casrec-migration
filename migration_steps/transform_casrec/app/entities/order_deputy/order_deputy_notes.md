SQL equivalent:

```sql
with persons_df as (
    select id, c_deputy_no
    from etl2.persons
    where type = 'actor_deputy'
),

deputyship_df as (
    select "Deputy No", "Case", "Order No"
    from etl1.deputyship
),

cases_df as (
    select id, caserecnumber, c_order_no
    from etl2.cases
)

select * from persons_df
    inner join deputyship_df on persons_df.c_deputy_no = deputyship_df."Deputy No"
    inner join cases_df on cases_df.caserecnumber = deputyship_df."Case" and cases_df.c_order_no = deputyship_df."Order No"
```
