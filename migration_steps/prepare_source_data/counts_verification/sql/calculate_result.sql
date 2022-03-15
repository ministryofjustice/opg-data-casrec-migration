SELECT
    supervision_table,

    -- lpa
    CASE WHEN lpa_pre_delete IS NULL THEN 'n/a'
    ELSE
        CASE
            WHEN (lpa_post_delete != lpa_pre_delete OR lpa_post_delete IS NULL) THEN 'DELETE ERROR'
            WHEN supervision_table = 'scheduled_events' THEN 'DELETE - OK'
            WHEN (lpa_post_migrate != lpa_post_delete OR lpa_post_migrate IS NULL) THEN 'MIGRATE ERROR'
            ELSE 'OK'
        END
    END AS  lpa_status,

    -- cp1
    CASE WHEN cp1_pre_delete IS NULL THEN 'n/a'
    ELSE
        CASE
            WHEN (cp1_post_delete != cp1_pre_delete OR cp1_post_delete IS NULL) THEN 'DELETE ERROR'
            WHEN supervision_table in ('feepayer_id', 'person_document', 'finance_person') THEN 'DELETE - OK'
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
            WHEN non_cp1_post_delete > 0 AND supervision_table NOT IN ('persons_clients', 'finance_person', 'person_document')
            THEN 'DELETE ERROR'
            WHEN non_cp1_post_delete != non_cp1_pre_delete AND supervision_table IN ('persons_clients', 'finance_person')
            THEN 'DELETE ERROR'
            WHEN
                (non_cp1_pre_delete + (
                    SELECT non_cp1_pre_delete FROM {count_schema}.counts WHERE supervision_table = 'caseitem_document')
                ) != non_cp1_post_delete AND supervision_table IN ('person_document')
            THEN 'DELETE ERROR'
            ELSE 'OK'
        END
    END AS  non_cp1_status
FROM {count_schema}.counts
ORDER BY supervision_table;
