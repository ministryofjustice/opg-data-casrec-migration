-- 1. New schema per update pmf_[table]_[field]_[date]_[Jira]
CREATE SCHEMA if not exists pmf_tasks_type_20220308_in1202;

-- 2. Build Update table: PK, caserecnumber, original value, expected value
SELECT tasks_id, sup_case AS caserecnumber, type AS original_value, 'VIRD' AS expected_value
INTO pmf_tasks_type_20220308_in1202.tasks_updates
FROM (
    SELECT
        sup_case,
        t.id AS tasks_id,
        t.type
    FROM (
        SELECT sa."Case" AS sup_case,
               sa."Sup Desc" AS sup_desc,
               sa."Start Date" AS sa_startdate,
               t2."Start Date" AS at_start_date
        FROM casrec_csv.sup_activity sa
        LEFT JOIN  (
            SELECT "Case", "Start Date", "Sup ID", "Defn ID", rownum FROM (
                SELECT "Case",
                       "Start Date",
                       "Sup ID",
                       "Defn ID",
                       row_number()
                           OVER ( PARTITION BY at."Case", at."Sup ID", at."Defn ID" ORDER BY at.casrec_row_id DESC ) AS rownum
                FROM casrec_csv.activity_tracking at
            ) t1
            WHERE rownum = 1
        ) t2
        ON t2."Case" = sa."Case"
        AND t2."Sup ID" = sa."SupID"
        AND t2."Defn ID" = sa."DefnID"
        WHERE sa."Status" = 'ACTIVE'
        AND sa."Sup Desc" = 'URGENT VISIT REPORT'
        ORDER BY sa."Case" ASC
    ) casrec
    INNER JOIN persons p ON p.caserecnumber = sup_case
    INNER JOIN person_task pt ON pt.person_id = p.id
    INNER JOIN tasks t ON t.id = pt.task_id
    WHERE t.duedate = CAST(at_start_date AS DATE)
    ORDER BY sup_case
) update_wrapper;


-- 3. Build Audit Table - a complete snapshot of each row affected
SELECT t.*
INTO pmf_tasks_type_20220308_in1202.tasks_audit
FROM pmf_tasks_type_20220308_in1202.tasks_updates tu
INNER JOIN tasks t ON t.id = tu.tasks_id;


-- 4. Perform Update
BEGIN;
    UPDATE tasks t SET type = tu.expected_value
    FROM pmf_tasks_type_20220308_in1202.tasks_updates tu
    WHERE tu.tasks_id = t.id;

-- Rollback OR Commit
-- affected row count looks BAD: back out
ROLLBACK;
-- OR
-- affected row count correct: commit
COMMIT;


-- 5. Validation
-- Validation script (should be 0)
SELECT tasks_id, expected_value
FROM pmf_tasks_type_20220308_in1202.tasks_updates tu
EXCEPT
SELECT t.id, t.type
FROM tasks t
INNER JOIN pmf_tasks_type_20220308_in1202.tasks_audit au
ON au.id = t.id;
