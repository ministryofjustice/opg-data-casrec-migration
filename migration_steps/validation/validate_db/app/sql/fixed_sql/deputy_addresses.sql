-- deputy_addresses

DROP TABLE IF EXISTS {casrec_schema}.exceptions_deputy_addresses;

CREATE TABLE {casrec_schema}.exceptions_deputy_addresses(
    caserecnumber text default NULL,
    casesubtype text default NULL,
    orderdate text default NULL,
    address_lines text default NULL,
    town text default NULL,
    county text default NULL,
    postcode text default NULL,
    country text default NULL,
    type text default NULL,
    isairmailrequired text default NULL
);

SET datestyle = "ISO, DMY";

INSERT INTO {casrec_schema}.exceptions_deputy_addresses(
    SELECT * FROM (
        SELECT DISTINCT
            da2.person_id AS person_id,
            CONCAT({casrec_schema}.deputy_address."Dep Adrs1", ',', {casrec_schema}.deputy_address."Dep Adrs2") AS address_lines,
            NULLIF(TRIM({casrec_schema}.deputy_address."Dep Adrs3"), '') AS town,
            NULLIF(TRIM({casrec_schema}.deputy_address."Dep Adrs4"), '') AS county,
            NULLIF(TRIM({casrec_schema}.deputy_address."Dep Postcode"), '') AS postcode,
            NULLIF(TRIM({casrec_schema}.deputy_address."Dep Adrs5"), '') AS country,
            CASE WHEN deputy_address."Dep Addr No" IS NULL THEN NULL ELSE 'Primary' END AS type,
            transf_convert_to_bool({casrec_schema}.deputy_address."Foreign") AS isairmailrequired
        FROM {casrec_schema}.deputy_address
        INNER JOIN {casrec_schema}.deputyship ON {casrec_schema}.deputy_address."Dep Addr No" = {casrec_schema}.deputyship."Dep Addr No"
        INNER JOIN {casrec_schema}.order ON {casrec_schema}.deputyship."Order No" = {casrec_schema}.order."Order No"
        INNER JOIN (
            SELECT DISTINCT person_id, "Dep Addr No" FROM (
                select p.id as person_id, dl."Dep Addr No"
                from {casrec_schema}.deplink dl
                inner join {casrec_schema}.deputy d on d."Deputy No" = dl."Deputy No"
                inner join {target_schema}.persons p on CAST(p.deputynumber AS INT) = CAST(d."Deputy No" AS INT)
                WHERE dl."Main Addr" = '1'
                AND d."Dep Type" IN ('20', '21', '22', '24', '25', '26', '27', '28', '29', '63', '71')
                AND p.clientsource = '{client_source}'

                UNION

                SELECT p.id AS person_id, ds."Dep Addr No"
                FROM {casrec_schema}.deputy d
                INNER JOIN {target_schema}.persons p
                ON CAST(d."Deputy No" AS INT) = CAST(p.deputynumber AS INT)
                INNER JOIN {casrec_schema}.deputyship ds
                ON d."Deputy No" = ds."Deputy No"
                WHERE d."Dep Type" NOT IN ('20', '21', '22', '24', '25', '26', '27', '28', '29', '63', '71')
                AND p.clientsource = '{client_source}'
            ) da
        ) da2
        ON {casrec_schema}.deputy_address."Dep Addr No" = da2."Dep Addr No"
        WHERE {casrec_schema}.order."Ord Stat" != 'Open'
    ) as csv_data

    EXCEPT

    SELECT * FROM (
        SELECT DISTINCT
            persons.id AS person_id,
            array_to_string(ARRAY(SELECT json_array_elements_text(addresses.address_lines)), ',') AS address_lines,
            NULLIF(TRIM(addresses.town), '') AS town,
            NULLIF(TRIM(addresses.county), '') AS county,
            NULLIF(TRIM(addresses.postcode), '') AS postcode,
            NULLIF(TRIM(addresses.country), '') AS country,
            NULLIF(TRIM(addresses.type), '') AS type,
            addresses.isairmailrequired AS isairmailrequired
        FROM {target_schema}.order_deputy
        INNER JOIN {target_schema}.cases ON cases.id = order_deputy.order_id
        INNER JOIN {target_schema}.persons ON persons.id = order_deputy.deputy_id
        INNER JOIN {target_schema}.addresses ON addresses.person_id = persons.id
        WHERE persons.type = 'actor_deputy'
        AND persons.clientsource = '{client_source}'
    ) as sirius_data
);
