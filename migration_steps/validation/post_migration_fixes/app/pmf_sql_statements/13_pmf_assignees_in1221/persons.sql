--Purpose: Update supervisioncaseowner_id based on the teams given in matrix spreadsheet
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

CREATE TABLE IF NOT EXISTS {pmf_schema}.corref_to_team (corref varchar(10), team varchar(100));

INSERT INTO {pmf_schema}.corref_to_team (corref, team)
VALUES
('A1','Public Authority Deputy Team'),
('A2','Public Authority Deputy Team'),
('A2A','Public Authority Deputy Team'),
('A3','Public Authority Deputy Team'),
('A3G','Public Authority Deputy Team'),
('ADC','Public Authority Deputy Team'),
('ARD','Supervision Closed Cases'),
('C1','Legal Team Deputyships'),
('DCC','Supervision Closed Cases'),
('DCS','Deputyship Investigations'),
('DOD','Supervision Closed Cases'),
('FOE','Supervision Closed Cases'),
('HW','Health and Welfare Team'),
('L1','Lay Team 1'),
('L2','Lay Team 1'),
('L2A','Lay Team 1'),
('L3','Lay Team 1'),
('L3G','Lay Team 1'),
('LDC','Lay Team 1'),
('ODP','Supervision Closed Cases'),
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
('RGY','Supervision Closed Cases'),
('S1A','Deputyship Investigations'),
('S1N','Deputyship Investigations'),
('NA', 'Supervision Closed Cases'),
('NEW', 'Supervision Closed Cases');

WITH pro_dep_owner AS (
    SELECT "Case", "DPfcw"
    FROM
    (
        SELECT
        row_number() over (partition BY p."Case" ORDER BY CASE WHEN ds."Fee Payer" = 'Y' THEN 1 ELSE 0 END desc, ds."Create" desc) as rown,
        p."Case", d."DPfcw", ds."Create", ds."Fee Payer"
        FROM {casrec_schema}.pat p
        INNER JOIN {casrec_schema}.order o ON p."Case" = o."Case"
        INNER JOIN {casrec_schema}.deputyship ds ON o."Order No" = ds."Order No"
        INNER JOIN {casrec_schema}.deputy d ON d."Deputy No" = ds."Deputy No"
        WHERE d."Dep Type" in ('20','21','22','24','25','26','27','28','29','63','71')
        and p."Corref" in ('P1','P2','P2A','P3','P3G','PDC')
        and o."Ord Stat" = 'Active'
        and d."DPfcw" != ''
    ) as a
    WHERE rown = 1
), pa_dep_owner AS (
    SELECT "Case", "DPfcw"
    FROM
    (
        SELECT
        row_number() over (partition BY p."Case" ORDER BY CASE WHEN ds."Fee Payer" = 'Y' THEN 1 ELSE 0 END desc, ds."Create" desc) as rown,
        p."Case", d."DPfcw", ds."Create", ds."Fee Payer"
        FROM {casrec_schema}.pat p
        INNER JOIN {casrec_schema}.order o ON p."Case" = o."Case"
        INNER JOIN {casrec_schema}.deputyship ds ON o."Order No" = ds."Order No"
        INNER JOIN {casrec_schema}.deputy d ON d."Deputy No" = ds."Deputy No"
        WHERE d."Dep Type" in ('23')
        and p."Corref" in ('A1','A2','A2A','A3','A3G')
        and o."Ord Stat" = 'Active'
        and d."DPfcw" != ''
    ) as a
    WHERE rown = 1
),
lookup_table AS
(
    SELECT
    caserecnumber as caserecnumber,
    person_id,
    corref,
    supervisioncaseowner_id as original_value,
    pro_dep_ass_name,
    pro_dep_team_name,
    pro_dep_ass_id,
    pa_dep_ass_name,
    pa_dep_team_name,
    pa_dep_ass_id,
    team_map,
    default_team_id,
    default_team_name,
    terminated,
    actual_ass_name,
    actual_ass_team,
    actual_ass_id
    FROM
    (
        SELECT per.caserecnumber, per.id, per.supervisioncaseowner_id,
        pat."Corref" as corref,
        per.id as person_id,
        ctt.team as team_map,
        a.id as default_team_id,
        a.name as default_team_name,
        pro_dep_ass.name as pro_dep_ass_name,
        pro_dep_ass_team.name as pro_dep_team_name,
        pro_dep_ass.id as pro_dep_ass_id,
        pa_dep_ass.name as pa_dep_ass_name,
        pa_dep_ass_team.name as pa_dep_team_name,
        pa_dep_ass.id as pa_dep_ass_id,
        CASE WHEN "Term Date" != '' THEN 1 ELSE 0 END as terminated,
        ac_ass.name as actual_ass_name,
        ac_ass_team.name as actual_ass_team,
        ac_ass.id as actual_ass_id
        FROM persons per
        INNER JOIN {casrec_schema}.pat pat on pat."Case" = per.caserecnumber
        LEFT JOIN {pmf_schema}.corref_to_team ctt on pat."Corref" = ctt.corref
        LEFT JOIN assignees a on a.name = ctt.team
        LEFT JOIN assignees ac_ass on {casrec_schema}.assignee_lookup(pat."PFCWorker") = ac_ass.id
        LEFT JOIN assignee_teams a_team on a_team.assignablecomposite_id = ac_ass.id
        LEFT JOIN assignees ac_ass_team on ac_ass_team.id = a_team.team_id
        LEFT JOIN pro_dep_owner pdo on pdo."Case" = pat."Case"
        LEFT JOIN assignees pro_dep_ass on {casrec_schema}.assignee_lookup(pdo."DPfcw") = pro_dep_ass.id
        LEFT JOIN assignee_teams pro_dep_team on pro_dep_team.assignablecomposite_id = pro_dep_ass.id
        LEFT JOIN assignees pro_dep_ass_team on pro_dep_ass_team.id = pro_dep_team.team_id
        LEFT JOIN pa_dep_owner pado on pado."Case" = pat."Case"
        LEFT JOIN assignees pa_dep_ass on {casrec_schema}.assignee_lookup(pado."DPfcw") = pa_dep_ass.id
        LEFT JOIN assignee_teams pa_dep_team on pa_dep_team.assignablecomposite_id = pa_dep_ass.id
        LEFT JOIN assignees pa_dep_ass_team on pa_dep_ass_team.id = pa_dep_team.team_id
    ) as updates
), final_lookup as
(
    SELECT
    caserecnumber,
    person_id,
    corref,
    original_value,
    pro_dep_ass_name,
    pro_dep_team_name,
    pro_dep_ass_id,
    pa_dep_ass_name,
    pa_dep_team_name,
    pa_dep_ass_id,
    team_map,
    default_team_id,
    default_team_name,
    terminated,
    actual_ass_name,
    actual_ass_team,
    actual_ass_id,
    CASE
    WHEN corref in ('A1', 'A2', 'A2A', 'A3', 'A3G') AND coalesce(actual_ass_team, '') like 'Public Authority%'
    THEN actual_ass_id
    WHEN corref in ('A1', 'A2', 'A2A', 'A3', 'A3G') AND coalesce(actual_ass_team, '') not like 'Public Authority%'
    AND coalesce(pa_dep_team_name, '') like 'Public Authority%'
    THEN pa_dep_ass_id
    WHEN corref in ('A1', 'A2', 'A2A', 'A3', 'A3G') AND coalesce(actual_ass_team, '') not like 'Public Authority%'
    AND coalesce(pa_dep_team_name, '') not like 'Public Authority%'
    THEN default_team_id
    WHEN corref in ('HW') AND coalesce(actual_ass_team, '') like 'Health and Welfare%'
    THEN actual_ass_id
    WHEN corref in ('HW') AND coalesce(actual_ass_team, '') not like 'Health and Welfare%'
    THEN default_team_id
    WHEN corref in ('L3', 'L2', 'L1', 'L2A', 'L3G') AND coalesce(actual_ass_team, '') like 'Lay%'
    THEN actual_ass_id
    WHEN corref in ('L3', 'L2', 'L1', 'L2A', 'L3G') AND coalesce(actual_ass_team, '') not like 'Lay%'
    THEN default_team_id
    WHEN corref in ('P1','P2','P2A','P3','P3G') AND coalesce(actual_ass_team, '') like 'Prof%'
    THEN actual_ass_id
    WHEN corref in ('P1','P2','P2A','P3','P3G') AND coalesce(actual_ass_team, '') not like 'Prof%'
    AND coalesce(pro_dep_team_name, '') LIKE 'Prof%'
    THEN pro_dep_ass_id
    WHEN corref in ('P1','P2','P2A','P3','P3G') AND coalesce(actual_ass_team, '') not like 'Prof%'
    AND coalesce(pro_dep_team_name, '') NOT LIKE 'Prof%'
    THEN default_team_id
    WHEN corref in ('PDC') AND terminated = 1
    THEN (SELECT id FROM assignees WHERE name = 'Supervision Closed Cases')
    WHEN corref in ('PDC') AND coalesce(actual_ass_team, '') like 'Prof%'
    THEN actual_ass_id
    WHEN corref in ('PDC') AND coalesce(actual_ass_team, '') not like 'Prof%'
    AND coalesce(pro_dep_team_name, '') LIKE 'Prof%'
    THEN pro_dep_ass_id
    WHEN corref in ('PDC') AND coalesce(actual_ass_team, '') not like 'Prof%'
    AND coalesce(pro_dep_team_name, '') NOT LIKE 'Prof%'
    THEN default_team_id
    WHEN corref in ('ADC') AND terminated = 1
    THEN (SELECT id FROM assignees WHERE name = 'Supervision Closed Cases')
    WHEN corref in ('ADC')
    THEN default_team_id
    WHEN corref in ('LDC') AND terminated = 1
    THEN (SELECT id FROM assignees WHERE name = 'Supervision Closed Cases')
    WHEN corref in ('LDC') AND coalesce(actual_ass_team, '') like 'Lay%'
    THEN actual_ass_id
    WHEN corref in ('LDC') AND coalesce(actual_ass_team, '') not like 'Lay%'
    THEN default_team_id
    WHEN corref in ('ARD','C1','DCC','DCS','DOD','FOE','ODP','ORS','ORV','PGA','PGC','PGH','PGR','RGY','S1A','S1N','NA','NEW')
    THEN default_team_id
    END as expected_id
    FROM lookup_table
)
SELECT
caserecnumber,
person_id,
corref,
original_value,
pro_dep_ass_name,
pro_dep_team_name,
pro_dep_ass_id,
pa_dep_ass_name,
pa_dep_team_name,
pa_dep_ass_id,
team_map,
default_team_id,
default_team_name,
terminated,
actual_ass_name,
actual_ass_team,
actual_ass_id,
expected_id,
a.name as expected_name,
ac_ass_team.name as expected_team_name
INTO {pmf_schema}.persons_updates
FROM final_lookup f
LEFT JOIN assignees a on a.id = f.expected_id
LEFT JOIN assignee_teams a_team on a_team.assignablecomposite_id = a.id
LEFT JOIN assignees ac_ass_team on ac_ass_team.id = a_team.team_id;

--@audit_tag
SELECT p.*
INTO {pmf_schema}.persons_audit
FROM {pmf_schema}.persons_updates u
INNER JOIN persons p on p.id = u.person_id;

--@update_tag
UPDATE persons p SET supervisioncaseowner_id = u.expected_id
FROM {pmf_schema}.persons_updates u
WHERE u.person_id = p.id
and u.original_value != u.expected_id;

--@validate_tag
SELECT caserecnumber, expected_id
FROM {pmf_schema}.persons_updates
EXCEPT
SELECT p.caserecnumber, p.supervisioncaseowner_id
FROM persons p
INNER JOIN {pmf_schema}.persons_audit a
ON a.id = p.id;