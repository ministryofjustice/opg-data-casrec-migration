--@setup_tag
CREATE SCHEMA if not exists {pmf_schema};

SELECT tasks_id, sup_case AS caserecnumber, type AS original_value, 'VIRD' AS expected_value
INTO {pmf_schema}.tasks_updates
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
        FROM {casrec_schema}.sup_activity sa
        LEFT JOIN  (
            SELECT "Case", "Start Date", "Sup ID", "Defn ID", rownum FROM (
                SELECT "Case",
                       "Start Date",
                       "Sup ID",
                       "Defn ID",
                       row_number()
                           OVER ( PARTITION BY at."Case", at."Sup ID", at."Defn ID" ORDER BY at.casrec_row_id DESC ) AS rownum
                FROM {casrec_schema}.activity_tracking at
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

--@audit_tag
SELECT t.*
INTO {pmf_schema}.tasks_audit
FROM {pmf_schema}.tasks_updates tu
INNER JOIN tasks t ON t.id = tu.tasks_id;

--@update_tag
UPDATE tasks t SET type = tu.expected_value
FROM {pmf_schema}.tasks_updates tu
WHERE tu.tasks_id = t.id;

--@validate_tag
SELECT tasks_id, expected_value
FROM {pmf_schema}.tasks_updates tu
EXCEPT
SELECT t.id, t.type
FROM tasks t
INNER JOIN {pmf_schema}.tasks_audit au
ON au.id = t.id;
