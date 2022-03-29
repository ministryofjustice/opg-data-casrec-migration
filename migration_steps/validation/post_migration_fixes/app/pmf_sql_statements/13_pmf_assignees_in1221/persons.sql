--Purpose: Update supervisioncaseowner_id based on the teams given in matrix spreadsheet
--@setup_tag
CREATE TABLE IF NOT EXISTS {casrec_mapping}.corref_to_team (corref varchar(10), team varchar(100));

INSERT INTO {casrec_mapping}.corref_to_team (corref, team)
VALUES
('A1','Public Authority Deputy Team'),
('A2','Public Authority Deputy Team'),
('A2A','Public Authority Deputy Team'),
('A3','Public Authority Deputy Team'),
('A3G','Public Authority Deputy Team'),
('ADC','Public Authority Deputy Team'),
('ARD','Supervision Closed Cases team'),
('C1','Legal Team Deputyships'),
('DCC','Supervision Closed Cases team'),
('DCS','Deputyship Investigations'),
('DOD','Supervision Closed Cases team'),
('FOE','Supervision Closed Cases team'),
('HW','Health and Welfare Team'),
('L1','Lay Team 1'),
('L2','Lay Team 1'),
('L2A','Lay Team 1'),
('L3','Lay Team 1'),
('L3G','Lay Team 1'),
('LDC','Lay Team 1'),
('ODP','Supervision Closed Cases team'),
('ORS','Legal Team Deputyships'),
('ORV','Legal Team Deputyships'),
('P1','Professional Team 1'),
('P2','Professional Team 1'),
('P2A','Professional Team 1'),
('P3','Professional Team 1'),
('P3G','Professional Team 1'),
('PDC','Professional Team 1'),
('PGA','Legal Team Deputyships'),
('PGC','Legal Team Deputyships'),
('PGH','Legal Team Deputyships'),
('PGR','Legal Team Deputyships'),
('RGY','Supervision Closed Cases team'),
('S1A','Deputyship Investigations'),
('S1N','Deputyship Investigations'),
('NA',  'Supervision Closed Cases team'),
('NEW', 'Supervision Closed Cases team');

CREATE SCHEMA IF NOT EXISTS {pmf_schema};

SELECT
caserecnumber as caserecnumber,
id as person_id,
supervisioncaseowner_id as original_value,
ass_id as expected_value
INTO {pmf_schema}.persons_updates
FROM
(
    SELECT per.caserecnumber, per.id, per.supervisioncaseowner_id, pat."Corref" as corref, ctt.team, a.id as ass_id
    FROM persons per
    INNER JOIN {casrec_schema}.pat pat on pat."Case" = per.caserecnumber
    INNER JOIN {casrec_mapping}.corref_to_team ctt on pat."Corref" = ctt.corref
    LEFT JOIN assignees a on a.name = ctt.team
    WHERE per.supervisioncaseowner_id = 2657
) as updates;

--@audit_tag
SELECT p.*
INTO {pmf_schema}.persons_audit
FROM {pmf_schema}.persons_updates u
INNER JOIN persons p on p.id = u.person_id;

--@update_tag
UPDATE persons p SET supervisioncaseowner_id = u.expected_value
FROM {pmf_schema}.persons_updates u
WHERE u.person_id = p.id;

--@validate_tag
SELECT caserecnumber, expected_value
FROM {pmf_schema}.persons_updates
EXCEPT
SELECT p.caserecnumber, p.supervisioncaseowner_id
FROM persons p
INNER JOIN {pmf_schema}.persons_audit a
ON a.id = p.id;