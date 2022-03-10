-- sirius_letters
-- Simulate Sirius sending automated letters on a given date

INSERT INTO automated_letters.sirius(report_log_id, letter_type, letter_date, caserecnumber)
SELECT a0_.id, 'BS1', {letter_date}, p.caserecnumber
FROM {target_schema}.annual_report_logs a0_
         LEFT JOIN {target_schema}.cases c1_ ON a0_.order_id = c1_.id
    AND c1_.type IN ('order')
         LEFT JOIN {target_schema}.annual_report_lodging_details a2_ ON a0_.id = a2_.annual_report_log_id
         LEFT JOIN {target_schema}.annual_report_letter_status a3_ ON a0_.id = a3_.annualreport_id
    AND (a3_.templateId = 'BS1')
    INNER JOIN {target_schema}.persons p ON p.id = a0_.client_id
WHERE c1_.orderStatus = 'ACTIVE'
  AND p.clientsource = '{clientsource}'
  AND a2_.bankStatementDeadlineDate >= {bs1_from}
  AND a2_.bankStatementDeadlineDate <= {bs1_to}
  AND a2_.lodgedStatus = 'REFERRED_FOR_REVIEW'
  AND a2_.bankStatementsReceived <> true
  AND (a3_.id IS NULL
    OR (a3_.status NOT IN ('IN_PROGRESS', 'PROCESSED', 'ERROR')
        OR a3_.status IS NULL));


INSERT INTO automated_letters.sirius(report_log_id, letter_type, letter_date, caserecnumber)
SELECT a0_.id, 'BS2', {letter_date}, p.caserecnumber
FROM {target_schema}.annual_report_logs a0_
         LEFT JOIN {target_schema}.cases c1_ ON a0_.order_id = c1_.id
    AND c1_.type IN ('order')
         LEFT JOIN {target_schema}.annual_report_lodging_details a2_ ON a0_.id = a2_.annual_report_log_id
         LEFT JOIN {target_schema}.annual_report_letter_status a3_ ON a0_.id = a3_.annualreport_id
    AND (a3_.templateId = 'BS2')
    INNER JOIN {target_schema}.persons p ON p.id = a0_.client_id
WHERE c1_.orderStatus = 'ACTIVE'
  AND p.clientsource = '{clientsource}'
  AND a2_.bankStatementDeadlineDate >= {bs2_from}
  AND a2_.bankStatementDeadlineDate <= {bs2_to}
  AND a2_.lodgedStatus = 'REFERRED_FOR_REVIEW'
  AND a2_.bankStatementsReceived <> true
  AND (a3_.id IS NULL
    OR (a3_.status NOT IN ('IN_PROGRESS','PROCESSED','ERROR')
        OR a3_.status IS NULL));


INSERT INTO automated_letters.sirius(report_log_id, letter_type, letter_date, caserecnumber)
SELECT a0_.id, 'RD1', {letter_date}, p.caserecnumber
FROM {target_schema}.annual_report_logs a0_
         LEFT JOIN {target_schema}.cases c1_ ON a0_.order_id = c1_.id
    AND c1_.type IN ('order')
         LEFT JOIN {target_schema}.annual_report_letter_status a2_ ON a0_.id = a2_.annualreport_id
    AND (a2_.templateId = 'RD1')
    INNER JOIN {target_schema}.persons p ON p.id = a0_.client_id
WHERE c1_.orderStatus = 'ACTIVE'
  AND p.clientsource = '{clientsource}'
  AND a0_.reportingPeriodEndDate >= {rd1_from}
  AND a0_.reportingPeriodEndDate <= {rd1_to}
  AND (a2_.id IS NULL
    OR (a2_.status NOT IN ('IN_PROGRESS','PROCESSED','ERROR')
        OR a2_.status IS NULL));


INSERT INTO automated_letters.sirius(report_log_id, letter_type, letter_date, caserecnumber)
SELECT a0_.id, 'RD2', {letter_date}, p.caserecnumber
FROM {target_schema}.annual_report_logs a0_
         LEFT JOIN {target_schema}.cases c1_ ON a0_.order_id = c1_.id
    AND c1_.type IN ('order')
         LEFT JOIN {target_schema}.annual_report_letter_status a2_ ON a0_.id = a2_.annualreport_id
    AND (a2_.templateId = 'RD2')
    INNER JOIN {target_schema}.persons p ON p.id = a0_.client_id
WHERE c1_.orderStatus = 'ACTIVE'
  AND p.clientsource = '{clientsource}'
  AND a0_.reportingPeriodEndDate >= {rd2_from}
  AND a0_.reportingPeriodEndDate <= {rd2_to}
  AND a0_.status = 'DUE'
  AND (a2_.id IS NULL
    OR (a2_.status NOT IN ('IN_PROGRESS','PROCESSED','ERROR')
        OR a2_.status IS NULL));


INSERT INTO automated_letters.sirius(report_log_id, letter_type, letter_date, caserecnumber)
SELECT a0_.id, 'RI2', {letter_date}, p.caserecnumber
FROM {target_schema}.annual_report_logs a0_
         LEFT JOIN {target_schema}.cases c1_ ON a0_.order_id = c1_.id
    AND c1_.type IN ('order')
         LEFT JOIN {target_schema}.annual_report_lodging_details a2_ ON a0_.id = a2_.annual_report_log_id
         LEFT JOIN {target_schema}.annual_report_letter_status a3_ ON a0_.id = a3_.annualreport_id
    AND (a3_.templateId = 'RI2')
    INNER JOIN {target_schema}.persons p ON p.id = a0_.client_id
WHERE c1_.orderStatus = 'ACTIVE'
  AND p.clientsource = '{clientsource}'
  AND a2_.deadlineDate >= {ri2_from}
  AND a2_.deadlineDate <= {ri2_to}
  AND a2_.resubmittedDate IS NULL
  AND (a3_.id IS NULL
    OR (a3_.status NOT IN ('IN_PROGRESS','PROCESSED','ERROR')
        OR a3_.status IS NULL));


INSERT INTO automated_letters.sirius(report_log_id, letter_type, letter_date, caserecnumber)
SELECT a0_.id, 'RI3', {letter_date}, p.caserecnumber
FROM {target_schema}.annual_report_logs a0_
         LEFT JOIN {target_schema}.cases c1_ ON a0_.order_id = c1_.id
    AND c1_.type IN ('order')
         LEFT JOIN {target_schema}.annual_report_lodging_details a2_ ON a0_.id = a2_.annual_report_log_id
         LEFT JOIN {target_schema}.annual_report_letter_status a3_ ON a0_.id = a3_.annualreport_id
    AND (a3_.templateId = 'RI3')
    INNER JOIN {target_schema}.persons p ON p.id = a0_.client_id
WHERE c1_.orderStatus = 'ACTIVE'
  AND p.clientsource = '{clientsource}'
  AND a2_.deadlineDate >= {ri3_from}
  AND a2_.deadlineDate <= {ri3_to}
  AND a2_.resubmittedDate IS NULL
  AND (a3_.id IS NULL
    OR (a3_.status NOT IN ('IN_PROGRESS','PROCESSED','ERROR')
        OR a3_.status IS NULL));


INSERT INTO automated_letters.sirius(report_log_id, letter_type, letter_date, caserecnumber)
SELECT a0_.id, 'RR1', {letter_date}, p.caserecnumber
FROM {target_schema}.annual_report_logs a0_
         LEFT JOIN {target_schema}.cases c1_ ON a0_.order_id = c1_.id
    AND c1_.type IN ('order')
         LEFT JOIN {target_schema}.annual_report_letter_status a2_ ON a0_.id = a2_.annualreport_id
    AND (a2_.templateId = 'RR1')
    INNER JOIN {target_schema}.persons p ON p.id = a0_.client_id
WHERE c1_.orderStatus = 'ACTIVE'
  AND p.clientsource = '{clientsource}'
  AND a0_.dueDate >= {rr1_from}
  AND a0_.dueDate <= {rr1_to}
  AND a0_.status = 'OVERDUE'
  AND (a2_.id IS NULL
    OR (a2_.status NOT IN ('IN_PROGRESS','PROCESSED','ERROR')
        OR a2_.status IS NULL));


WITH annual_reports_of_interest AS (
    SELECT ar.id                     AS annual_report_id,
           ar.reportingperiodenddate AS reporting_period_end_date,
           ar.order_id               AS order_id
    FROM {target_schema}.annual_report_logs ar
             LEFT JOIN {target_schema}.cases c ON ar.order_id = c.id AND c.type = 'order'
             LEFT JOIN {target_schema}.annual_report_letter_status ls ON ar.id = ls.annualreport_id AND (ls.templateId = 'RR2')
    WHERE c.orderStatus = 'ACTIVE'
      AND ar.status = 'OVERDUE'
      AND ar.revisedDueDate IS NULL
      AND ar.receiveddate IS NULL
      AND (ls.id IS NULL OR ls.status NOT IN ('IN_PROGRESS','PROCESSED','ERROR'))
),
deputy_types_on_order AS (
    SELECT distinct annual_report_id,
        annual_reports_of_interest.order_id,
        od.deputytype AS deputy_type,
        reporting_period_end_date
    FROM annual_reports_of_interest
        inner join {target_schema}.order_deputy od
    ON annual_reports_of_interest.order_id = od.order_id
),
order_has_pro_or_pa_deputy AS (
    WITH deputies AS (SELECT order_id, deputy_type FROM deputy_types_on_order)
    SELECT distinct deputies.order_id,
        exists (SELECT * from deputies WHERE (deputy_type IN ('PRO', 'PA')) and deputy_types_on_order.order_id = deputies.order_id) AS hasProOrPaDeputy
    FROM deputies LEFT JOIN deputy_types_on_order
    ON deputy_types_on_order.order_id = deputies.order_id
),
schedule_date_check AS (
    SELECT distinct hasProOrPaDeputy, order_has_pro_or_pa_deputy.order_id, annual_report_id
    FROM order_has_pro_or_pa_deputy
        LEFT JOIN deputy_types_on_order
    ON deputy_types_on_order.order_id = order_has_pro_or_pa_deputy.order_id
    WHERE (hasProOrPaDeputy = false
      AND
        (reporting_period_end_date >= {rr2_from_lay}
      AND reporting_period_end_date <= {rr2_to_lay}))
       OR (hasProOrPaDeputy = true
      AND (reporting_period_end_date >= {rr2_from_pro_pa}
      AND
        reporting_period_end_date <= {rr2_to_pro_pa}))
)
INSERT INTO automated_letters.sirius(report_log_id, letter_type, letter_date, caserecnumber)
SELECT annual_report_logs.id, 'RR2', {letter_date}, p.caserecnumber
FROM {target_schema}.annual_report_logs
INNER JOIN {target_schema}.persons p ON p.id = annual_report_logs.client_id
inner join schedule_date_check on annual_report_logs.id = schedule_date_check.annual_report_id
WHERE p.clientsource = '{clientsource}';


INSERT INTO automated_letters.sirius(report_log_id, letter_type, letter_date, caserecnumber)
SELECT a0_.id, 'RR3', {letter_date}, p.caserecnumber
FROM {target_schema}.annual_report_logs a0_
         LEFT JOIN {target_schema}.cases c1_ ON a0_.order_id = c1_.id
    AND c1_.type IN ('order')
         LEFT JOIN {target_schema}.annual_report_letter_status a2_ ON a0_.id = a2_.annualreport_id
    AND (a2_.templateId = 'RR3')
    INNER JOIN {target_schema}.persons p ON p.id = a0_.client_id
WHERE c1_.orderStatus = 'ACTIVE'
  AND p.clientsource = '{clientsource}'
  AND a0_.status = 'OVERDUE'
  AND a0_.revisedDueDate IS NOT NULL
  AND a0_.receiveddate IS NULL
  AND a0_.revisedDueDate >= {rr3_from}
  AND a0_.revisedDueDate <= {rr3_to}
  AND (a2_.id IS NULL
    OR (a2_.status NOT IN ('IN_PROGRESS','PROCESSED','ERROR')
        OR a2_.status IS NULL));
