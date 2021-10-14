-- record the last ledger entry and allocation IDs prior to importing payments
-- so that imported payments can be batched together
CREATE TABLE public.temp_payments_migration_last_ids AS
    SELECT MAX(le.id) as last_ledger_entry_id, MAX(lea.id) as last_ledger_entry_allocation_id
    FROM public.finance_ledger le
    LEFT JOIN public.finance_ledger_allocation lea ON le.id = lea.ledger_entry_id;

SELECT * FROM public.temp_payments_migration_last_ids;
