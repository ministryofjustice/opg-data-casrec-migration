-- CP1 mismatches not captured by main query
WITH AllocationsAndLayDuplicateTeams AS (
     SELECT p.id, p.firstname, p.surname, p.supervisioncaseowner_id, a.name, p.caseactorgroup, p.caserecnumber, 'alloc_duplicates_teams' as query_source
     FROM persons p
     INNER JOIN assignees a on a.id = p.supervisioncaseowner_id
     WHERE supervisioncaseowner_id in (2326, 6042)
     AND caseactorgroup = 'CLIENT-PILOT-ONE'
     ),
    AllDepuitesInLayHealthAndWelfareTeam AS (
         SELECT p.id, p.firstname, p.surname, p.supervisioncaseowner_id, a.name, p.caseactorgroup, p.caserecnumber, 'alloc_duplicates_teams' as query_source
         FROM assignees a
         LEFT JOIN assignee_teams ast on a.id = ast.assignablecomposite_id
         INNER JOIN persons p on a.id = p.supervisioncaseowner_id
         WHERE (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null)
         AND ast.team_id not in (2326, 6042, 1831)
         AND a.id not in (2326, 6042, 1831)
         )
SELECT * FROM AllDepuitesInLayHealthAndWelfareTeam
UNION
SELECT * FROM AllocationsAndLayDuplicateTeams;

-- Copy out all the CP1 clients to a file
\copy (SELECT p.caserecnumber as caserecnumber, p.firstname as firstname, p.surname as surname, p.supervisioncaseowner_id as supervisioncaseowner_id, p.caseactorgroup, a.name as assign_name FROM persons p LEFT JOIN assignees a on a.id = p.supervisioncaseowner_id WHERE p.type = 'actor_client' and p.caseactorgroup = 'CLIENT-PILOT-ONE') To '/tmp/cp1_cases.csv' With CSV DELIMITER ',' HEADER

-- Copy it over to load casrec DB and create a table for it to go in
CREATE TABLE casrec_csv.sirius_cp1_persons(caserecnumber text, firstname text, surname text, supervisioncaseowner_id text, name text, caseactorgroup text, assign_name text);

-- Copy it into the table
\copy casrec_csv.sirius_cp1_persons(caserecnumber, firstname, surname, supervisioncaseowner_id, name, caseactorgroup, assign_name) FROM '/tmp/cp1_cases.csv' DELIMITER ',' CSV HEADER

-- Run this select to find the differences
SELECT * INTO casrec_csv.cp1_srs_mismatch
FROM
(
    select casrec.*, ''
    FROM
    (select "Case" as caserecnumber,
    "Forename" as firstname,
    "Surname" as surname,
    "PFCWorker" as supervisioncaseowner_id,
    "Corref" as caseactorgroup,
    '' as assign_name
    'casrec_side_only' as source
    from casrec_csv.pat
    where "Corref" = 'SRS') as casrec
    LEFT JOIN
    (SELECT caserecnumber, firstname, surname, supervisioncaseowner_id, caseactorgroup, assign_name, ''
    FROM casrec_csv.sirius_cp1_persons) as sirius
    ON sirius.caserecnumber = casrec.caserecnumber
    WHERE sirius.caserecnumber is NULL
    UNION
    select sirius.*, casrec.caseactorgroup
    FROM
    (SELECT caserecnumber, firstname, surname, supervisioncaseowner_id, caseactorgroup, assign_name, 'sirius_side_only'
    FROM casrec_csv.sirius_cp1_persons) as sirius
    LEFT JOIN
    (select "Case" as caserecnumber,
    "Forename" as firstname,
    "Surname" as surname,
    "PFCWorker" as supervisioncaseowner_id,
    "Corref" as caseactorgroup,
    '' as assign_name
    '' as source
    from casrec_csv.pat) as casrec
    ON sirius.caserecnumber = casrec.caserecnumber
    WHERE coalesce(casrec.caseactorgroup, '') != 'SRS'
) as both_sides;

-- Copy them out to a file and upload to our S3 bucket
\copy (SELECT * FROM casrec_csv.cp1_srs_mismatch) TO '/tmp/case_result_set.csv' WITH CSV DELIMITER ',' HEADER;
