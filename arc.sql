select 'pat - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'pat'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'archive'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'archive'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'pat'
and table_schema = 'casrec_csv'
union all
select 'order - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'order'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcorder'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcorder'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'order'
and table_schema = 'casrec_csv'
union all
select 'account - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'account'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcaccount'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcaccount'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'account'
and table_schema = 'casrec_csv'
union all
select 'deputyship - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'deputyship'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcdeputyship'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcdeputyship'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'deputyship'
and table_schema = 'casrec_csv'
union all
select 'remarks - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'remarks'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcremarks'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcremarks'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'remarks'
and table_schema = 'casrec_csv'
union all
select 'repvis - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'repvis'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcrepvis'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcrepvis'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'repvis'
and table_schema = 'casrec_csv'
union all
select 'sup_activity - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'sup_activity'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcsup_activity'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcsup_activity'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'sup_activity'
and table_schema = 'casrec_csv'
union all
select 'feeexport - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'feeexport'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcfeeexport'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcfeeexport'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'feeexport'
and table_schema = 'casrec_csv'



select 'pat - live data - extra columns:'

select 'pat',
(select count(*) from casrec_csv.pat),
(select count(*) from casrec_csv.archive)
union all
select 'order',
(select count(*) from casrec_csv.order),
(select count(*) from casrec_csv.arcorder)
union all
select 'account',
(select count(*) from casrec_csv.account),
(select count(*) from casrec_csv.arcaccount)
union all
select 'deputyship',
(select count(*) from casrec_csv.deputyship),
(select count(*) from casrec_csv.arcdeputyship)
union all
select 'remarks',
(select count(*) from casrec_csv.remarks),
(select count(*) from casrec_csv.arcremarks)
union all
select 'repvis',
(select count(*) from casrec_csv.repvis),
(select count(*) from casrec_csv.arcrepvis)
union all
select 'feeexport',
(select count(*) from casrec_csv.feeexport),
(select count(*) from casrec_csv.arcfeeexport)


SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'archive'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'archive'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'pat'
and table_schema = 'casrec_csv'
union all
select 'order - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'order'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcorder'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcorder'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'order'
and table_schema = 'casrec_csv'
union all
select 'account - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'account'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcaccount'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcaccount'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'account'
and table_schema = 'casrec_csv'
union all
select 'deputyship - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'deputyship'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcdeputyship'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcdeputyship'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'deputyship'
and table_schema = 'casrec_csv'
union all
select 'remarks - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'remarks'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcremarks'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcremarks'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'remarks'
and table_schema = 'casrec_csv'
union all
select 'repvis - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'repvis'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcrepvis'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcrepvis'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'repvis'
and table_schema = 'casrec_csv'
union all
select 'sup_activity - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'sup_activity'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcsup_activity'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcsup_activity'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'sup_activity'
and table_schema = 'casrec_csv'
union all
select 'feeexport - live data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'feeexport'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcfeeexport'
and table_schema = 'casrec_csv'
union all
select 'pat - archive data - extra columns:'
union all
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'arcfeeexport'
and table_schema = 'casrec_csv'
except
SELECT lower(column_name)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'feeexport'
and table_schema = 'casrec_csv'