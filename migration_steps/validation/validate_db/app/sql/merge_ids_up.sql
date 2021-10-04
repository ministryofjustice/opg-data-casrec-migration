ALTER TABLE casrec_csv.deputy DROP COLUMN IF EXISTS sirius_id;
ALTER TABLE casrec_csv.deputy ADD sirius_id int;
UPDATE casrec_csv.deputy
    SET sirius_id = persons.id
    FROM integration.persons
    WHERE CAST(integration.persons.casrec_row_id AS INT) = deputy.casrec_row_id;
CREATE INDEX ON casrec_csv.deputy (sirius_id);
