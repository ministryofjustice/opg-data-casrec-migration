DELETE FROM addresses WHERE person_id > {max_orig_person_id};
DELETE FROM persons WHERE id > {max_orig_person_id};
-- DELETE FROM person_note WHERE person_id > {max_orig_person_id};
-- DELETE FROM person_caseitem WHERE person_id > {max_orig_person_id};
-- DELETE FROM notes WHERE id in (SELECT note_id FROM person_note WHERE person_id > {max_orig_person_id});
-- DELETE FROM cases WHERE client_id > {max_orig_person_id};
