ALTER TABLE {casrec_schema}.deputy DROP COLUMN IF EXISTS sirius_id;
ALTER TABLE {casrec_schema}.deputy ADD sirius_id int;
UPDATE {casrec_schema}.deputy
    SET sirius_id = persons.id
    FROM integration.persons
    WHERE CAST(integration.persons.casrec_row_id AS INT) = deputy.casrec_row_id
    AND integration.persons.type = 'actor_deputy';
CREATE INDEX ON {casrec_schema}.deputy (sirius_id);