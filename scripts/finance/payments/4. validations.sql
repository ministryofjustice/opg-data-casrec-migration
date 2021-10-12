-- get number of imported ledger entries and their batch number
SELECT batchnumber, COUNT(*) AS num_imported_ledger_entries
FROM public.finance_ledger
WHERE id > (SELECT last_ledger_entry_id FROM temp_payments_migration_last_ids)
GROUP BY batchnumber;

-- get number of imported ledger entry allocations and their batch number
SELECT batchnumber, COUNT(*) AS num_imported_ledger_entry_allocations
FROM public.finance_ledger_allocation
WHERE id > (SELECT last_ledger_entry_allocation_id FROM temp_payments_migration_last_ids)
GROUP BY batchnumber;

-- get number of batched payments, grouped and ordered by calendar date
SELECT
  DATE(le.datetime) AS payment_date,
  COUNT(le.batchnumber) AS num_batched_ledger_entries,
  SUM(CASE WHEN lea.batchnumber IS NULL THEN 0 ELSE 1 END) AS num_batched_ledger_entry_allocations
FROM public.finance_ledger le
LEFT JOIN public.finance_ledger_allocation lea ON le.id = lea.ledger_entry_id
WHERE le.batchnumber = (SELECT counter FROM public.finance_counter WHERE key = 'DatFileBatchNumberReportBatchNumber')
GROUP BY payment_date
ORDER BY payment_date ASC;