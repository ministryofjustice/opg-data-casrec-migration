-- Explanations and manual SQL we can run for migration count disparities

-- person_document: can't fully check filtered counts and deletions at same time
-- following should be equal to cp1_post_delete + non_cp1_post_delete:
SELECT COUNT(*)
FROM person_document pt
INNER JOIN persons p
ON p.id = pt.person_id
WHERE p.type = 'actor_client;

-- finance_person: can't fully check filtered counts and deletions at same time
-- following should be equal to cp1_post_delete + non_cp1_post_delete:
SELECT COUNT(*)
FROM finance_person fp
INNER JOIN persons p
ON p.id = fp.person_id
WHERE p.type = 'actor_client';

-- feepayer_id: out by 1 in validation and counts (post migration fix)

-- scheduled_events: migration validation handles complexity of validation (just checking deletes)