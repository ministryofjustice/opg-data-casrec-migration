ALTER TABLE countverification.counts DROP COLUMN IF EXISTS result;
ALTER TABLE countverification.counts ADD COLUMN result varchar(50);

UPDATE countverification.counts
SET result =
CASE WHEN cp1_post_delete != cp1_pre_delete THEN 'DELETE ERROR'
    WHEN non_cp1_post_delete > 0 THEN 'DELETE ERROR'
    WHEN lay_post_delete != lay_pre_delete THEN 'DELETE ERROR'
    WHEN lay_post_migrate != lay_post_delete THEN 'MIGRATE ERROR'
    WHEN cp1_post_migrate != (cp1_post_delete + casrec_pre_migrate) THEN 'MIGRATE ERROR'
    -- WHEN (casrec_source = -1 OR final_count = -1) THEN 'INCOMPLETE'
    ELSE 'OK'
END;
