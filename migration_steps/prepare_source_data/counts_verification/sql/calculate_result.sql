SELECT
    supervision_table,

    -- lpa
    CASE WHEN lpa_pre_delete IS NULL THEN 'n/a'
    ELSE
        CASE
            WHEN (lpa_post_delete != lpa_pre_delete OR lpa_post_delete IS NULL) THEN 'DELETE ERROR'
            WHEN (lpa_post_migrate != lpa_post_delete OR lpa_post_migrate IS NULL) THEN 'MIGRATE ERROR'
            ELSE 'OK'
        END
    END AS  lpa_status,

    -- cp1
    CASE WHEN cp1_pre_delete IS NULL THEN 'n/a'
    ELSE
        CASE
            WHEN (cp1_post_delete != cp1_pre_delete OR cp1_post_delete IS NULL) THEN 'DELETE ERROR'
            WHEN (
                cp1_post_migrate != (cp1_post_delete + casrec_pre_migrate)
                OR cp1_post_migrate IS NULL
                OR casrec_pre_migrate IS NULL
                ) THEN 'MIGRATE ERROR'
            ELSE 'OK'
        END
    END AS  cp1_status,

    -- non client-pilot-one
    CASE WHEN non_cp1_pre_delete IS NULL THEN 'n/a'
    ELSE
        CASE
            WHEN non_cp1_post_delete > 0 THEN 'DELETE ERROR'
            ELSE 'OK'
        END
    END AS  non_cp1_status

FROM countverification.counts
ORDER BY supervision_table
;
