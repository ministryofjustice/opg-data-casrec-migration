-- create a new batch number to be used for payments ledger entries and allocations
UPDATE public.finance_counter
SET counter = counter + 1
WHERE key = 'DatFileBatchNumberReportBatchNumber';

-- set batch number on ledger entries
UPDATE public.finance_ledger fl
SET batchnumber = counter
FROM public.finance_counter fc
WHERE fc.key = 'DatFileBatchNumberReportBatchNumber'
AND fl.id > (SELECT last_ledger_entry_id FROM temp_payments_migration_last_ids);

-- set batch number on ledger entry allocations
UPDATE public.finance_ledger_allocation fla
SET batchnumber = counter
FROM public.finance_counter fc
WHERE fc.key = 'DatFileBatchNumberReportBatchNumber'
AND fla.id > (SELECT last_ledger_entry_allocation_id FROM temp_payments_migration_last_ids);