-- finance_person_ids
-- Check that all finance entities have a finance_person_id

DROP TABLE IF EXISTS {casrec_schema}.exceptions_finance_person_ids;

CREATE TABLE {casrec_schema}.exceptions_finance_person_ids(
    caserecnumber text default NULL,
    sirius_table text default NULL,
    sirius_id text default NULL
);

INSERT INTO {casrec_schema}.exceptions_finance_person_ids(
    SELECT persons.caserecnumber, 'finance_invoice' AS sirius_table, finance_invoice.id AS sirius_id
    FROM {target_schema}.finance_invoice
    LEFT JOIN {target_schema}.persons ON persons.id = finance_invoice.person_id
    WHERE finance_invoice.finance_person_id IS NULL
    AND persons.clientsource = '{client_source}'

    UNION ALL

    SELECT NULL AS caserecnumber, 'finance_ledger' AS sirius_table, finance_ledger.id AS sirius_id
    FROM {target_schema}.finance_ledger
    WHERE finance_ledger.finance_person_id IS NULL
    AND finance_ledger.source = '{client_source}'

    UNION ALL

    SELECT persons.caserecnumber, 'finance_order' AS sirius_table, finance_order.id AS sirius_id
    FROM {target_schema}.finance_order
    LEFT JOIN {target_schema}.person_caseitem ON person_caseitem.caseitem_id = finance_order.order_id
    LEFT JOIN {target_schema}.persons ON persons.id = person_caseitem.person_id
    WHERE finance_order.finance_person_id IS NULL
    AND persons.clientsource = '{client_source}'

    UNION ALL

    SELECT NULL AS caserecnumber, 'finance_remission_exemption' AS sirius_table, finance_remission_exemption.id AS sirius_id
    FROM {target_schema}.finance_remission_exemption
    WHERE finance_remission_exemption.finance_person_id IS NULL
);
