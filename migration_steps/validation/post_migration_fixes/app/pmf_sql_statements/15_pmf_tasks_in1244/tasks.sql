--Purpose: Update caseownertask and assignee_id where assigneeID is Migration User. Used after Phase 1 and Phase 2
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

SELECT *
INTO {pmf_schema}.tasks_updates
FROM (
    SELECT
        tasks.id AS tasks_id,
        tasks.caseownertask AS caseownertask_original_value,
        True AS caseownertask_expected_value,
        tasks.assignee_id AS assignee_id_original_value,
        NULL AS assignee_id_expected_value
    FROM tasks
    LEFT JOIN caseitem_task ct
        ON ct.task_id = tasks.id
    LEFT JOIN cases c
        ON c.id = ct.caseitem_id
    LEFT JOIN persons p
        ON p.id = c.client_id
    WHERE tasks.assignee_id = 2657
    AND p.clientsource = '{client_source}'
) to_update;

--@audit_tag
SELECT *
INTO {pmf_schema}.tasks_audit
FROM (
    SELECT tasks.*
    FROM tasks
    LEFT JOIN caseitem_task ct
        ON ct.task_id = tasks.id
    LEFT JOIN cases c
        ON c.id = ct.caseitem_id
    LEFT JOIN persons p
        ON p.id = c.client_id
    WHERE tasks.assignee_id = 2657
    AND p.clientsource = '{client_source}'
) update_audit;

--@update_tag
UPDATE tasks t SET caseownertask = True
FROM {pmf_schema}.tasks_updates tu
WHERE tu.tasks_id = t.id;

UPDATE tasks t SET assignee_id = NULL
FROM {pmf_schema}.tasks_updates tu
WHERE tu.tasks_id = t.id;

--@validate_tag
SELECT
    tasks_id,
    caseownertask_expected_value,
    CAST(assignee_id_expected_value as INT)
FROM {pmf_schema}.tasks_updates tu
EXCEPT
SELECT t.id, t.caseownertask, t.assignee_id
FROM tasks t
INNER JOIN {pmf_schema}.tasks_audit a
    ON a.id = t.id;
