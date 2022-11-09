-- establish subset of client (with no cases) which have NO documents
SELECT cl.*
INTO deleted_cases_sw6081.clients_selection
FROM deleted_cases_sw6081.clients_nocases_no_documents cl
ORDER BY cl.id
LIMIT :runLimit
OFFSET :runOffset;

-- new run
INSERT INTO deleted_cases_sw6081.run (id, notes, selections_made_at, clients_affected)
VALUES (
    :runId,
    CONCAT(:'notePrefix', ' - LIMIT: ', :runLimit, ', OFFSET: ', :runOffset),
    CURRENT_TIMESTAMP(0),
    (SELECT COUNT(1) FROM deleted_cases_sw6081.clients_selection)
);

SELECT * FROM deleted_cases_sw6081.run;