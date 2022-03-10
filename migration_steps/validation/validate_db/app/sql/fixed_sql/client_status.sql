-- client_status
DROP TABLE IF EXISTS casrec_csv.exceptions_client_status;

CREATE TABLE casrec_csv.exceptions_client_status(
    caserecnumber text default NULL,
    clientstatus text default NULL
);

WITH pat_order AS (
    SELECT row_number() over (partition by p."Case" ORDER BY "Made Date" DESC) AS rown,
    CASE WHEN "Ord Stat" = 'Active' AND "Ord Type" IN ('26','43','45') THEN 'OPEN' ELSE UPPER("Ord Stat") END AS orderstatus,
    '' as orderclosurereason,
    p."Case" as caserecnumber,
    "Ord Type" AS ordersubtype,
    "Made Date" as orderdate
    FROM casrec_csv."order" o
    inner join casrec_csv."pat" p
    on p."Case" = o."Case"
    where "Ord Stat" != 'Open'
),
casrec_clientstatus_tbl as (
SELECT
client."Case" AS caserecnumber,
has_active_status.has_active_status AS has_active_status,
latest_status.status_latest AS latest_status,
identical_status.identical_status AS identical_status,
closed_dup_status.closed_dup_status AS closed_dup_status,
death_status.death_notified_status AS death_notified_status,
death_status.death_proof_status AS death_proof_status,
latest_status.closure_reason AS closure_reason,
latest_status.order_sub_type AS order_sub_type
FROM
casrec_csv.pat AS client
left join (
    SELECT
    "Case" as caserecnumber,
    CASE WHEN casrec_csv.pat."Notified" != '' then 'DEATH_NOTIFIED' end AS death_notified_status,
    CASE WHEN casrec_csv.pat."Proof" != '' then 'DEATH_CONFIRMED' end AS death_proof_status
    FROM casrec_csv.pat
    WHERE casrec_csv.pat."Term Type" = 'D'
) AS death_status on client."Case" = death_status.caserecnumber
left join (
    SELECT caserecnumber, orderstatus AS status_latest,
    orderclosurereason AS closure_reason, ordersubtype AS order_sub_type
    FROM (
        SELECT row_number() over (partition by caserecnumber ORDER BY orderdate DESC) AS rown,
        orderstatus,
        orderclosurereason,
        caserecnumber,
        ordersubtype
        FROM pat_order
    ) AS a
    WHERE rown = 1
) AS latest_status on latest_status.caserecnumber = client."Case"
left join (
    SELECT DISTINCT c.caserecnumber, c.orderstatus AS identical_status
    FROM pat_order c inner join
    (
        SELECT caserecnumber
        FROM pat_order
        group by caserecnumber
        having max(orderstatus) = min(orderstatus)
    ) AS co on c.caserecnumber = co.caserecnumber
) AS identical_status on identical_status.caserecnumber = client."Case"
left join (
    SELECT caserecnumber, 'CLOSED' AS closed_dup_status
    FROM pat_order
    group by caserecnumber
    having count(*) = count(
        CASE
        WHEN orderstatus = 'CLOSED' then 'X'
        WHEN orderstatus = 'DUPLICATE' then 'X'
        END
    )
) AS closed_dup_status on closed_dup_status.caserecnumber = client."Case"
left join (
        SELECT distinct
        orderstatus AS has_active_status,
        caserecnumber
        FROM pat_order
        WHERE orderstatus = 'ACTIVE'
) AS has_active_status on has_active_status.caserecnumber = client."Case"
order by caserecnumber),
casrec_final as (
    SELECT caserecnumber,
    CASE
        WHEN death_notified_status = 'DEATH_NOTIFIED' then 'DEATH_NOTIFIED'
        WHEN death_proof_status = 'DEATH_CONFIRMED' then 'DEATH_CONFIRMED'
        WHEN has_active_status = 'ACTIVE' then 'ACTIVE'
        WHEN latest_status = 'OPEN' then 'OPEN'
        WHEN closed_dup_status = 'CLOSED'
            and order_sub_type in ('1', '2', '41', '40', '26') then 'CLOSED'
        WHEN latest_status = 'CLOSED'
            and closure_reason = 'REGAINED_CAPACITY'
            then 'REGAINED_CAPACITY'
        WHEN latest_status = 'CLOSED'
            and closure_reason != 'REGAINED_CAPACITY'
            then 'INACTIVE'
        WHEN identical_status = 'DUPLICATE' then 'DUPLICATE'
    end as clientstatus
    from casrec_clientstatus_tbl
)
SELECT caserecnumber, clientstatus
FROM casrec_final
EXCEPT
SELECT caserecnumber, clientstatus
FROM {target_schema}.persons
WHERE persons.type = 'actor_client'
AND persons.clientsource = '{clientsource}';