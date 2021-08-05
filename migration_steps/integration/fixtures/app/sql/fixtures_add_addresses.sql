INSERT INTO addresses (id, person_id, address_lines, isairmailrequired) (
    SELECT (row_number() over ( order by id))*1000 as id,
           id as person_id, '["m","o","o"]' as address_lines, CAST(0 AS BOOLEAN) as isairmailrequired
    FROM persons
    WHERE clientsource = 'SKELETON'
    ORDER BY id DESC
);
