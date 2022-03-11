CREATE SCHEMA if not exists pmf_tasks_duedate_20220307_in1195;

SELECT tasks_id, tasks_duedate AS original_value, expected AS expected_value
INTO pmf_tasks_duedate_20220307_in1195.tasks_updates
FROM (
    SELECT
        casrec."Case",
        casrec.sup_activity_target         AS casrec_actual,
        t.id                               AS tasks_id,
        t.duedate                          AS tasks_duedate,
        casrec.activity_tracking_startdate AS expected
    FROM (
        SELECT
            sa."Case",
            sa."Start Date",
            sa."Target" AS sup_activity_target,
            t2."Start Date" AS activity_tracking_startdate
        FROM
        casrec_csv.sup_activity sa
        LEFT JOIN  (
            SELECT "Case", "Start Date", "Sup ID", "Defn ID", rownum FROM (
                SELECT "Case", "Start Date", "Sup ID", "Defn ID", row_number() OVER ( PARTITION BY at."Case", at."Sup ID", at."Defn ID" ORDER BY at.casrec_row_id DESC ) AS rownum
                FROM casrec_csv.activity_tracking at
            ) t1
            WHERE rownum = 1
        ) t2
        ON t2."Case" = sa."Case"
        AND t2."Sup ID" = sa."SupID"
        AND t2."Defn ID" = sa."DefnID"
        WHERE sa."Status" = 'ACTIVE'
        ORDER BY sa."Case" ASC
    ) casrec
    INNER JOIN persons p ON p.caserecnumber = casrec."Case"
    INNER JOIN person_task pt ON pt.person_id = p.id
    INNER JOIN tasks t ON t.id = pt.task_id AND t.duedate = CAST(casrec.sup_activity_target AS DATE)
    WHERE casrec.sup_activity_target != casrec.activity_tracking_startdate
) update_wrapper
;

SELECT t.*
INTO pmf_tasks_duedate_20220307_in1195.tasks_audit
FROM pmf_tasks_duedate_20220307_in1195.tasks_updates tu
INNER JOIN tasks t ON t.id = tu.tasks_id;

BEGIN;
    UPDATE tasks t SET duedate = CAST(tu.expected_value AS DATE)
    FROM pmf_tasks_duedate_20220307_in1195.tasks_updates tu
    WHERE tu.tasks_id = t.id;
-- Run if counts incorrect
ROLLBACK;
-- Run if counts correct
COMMIT;

-- Validation script (should be 0)
SELECT tasks_id, CAST(expected_value AS DATE)
FROM pmf_tasks_duedate_20220307_in1195.tasks_updates tu
EXCEPT
SELECT t.id, t.duedate
FROM tasks t
INNER JOIN pmf_tasks_duedate_20220307_in1195.tasks_audit au
    ON au.id = t.id;