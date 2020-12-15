-- Sirius entities are not tied to their sequence. Expect Sirius to fix this by the time of Migration
ALTER TABLE persons ALTER COLUMN id SET DEFAULT nextval('persons_id_seq');
ALTER TABLE addresses ALTER COLUMN id SET DEFAULT nextval('addresses_id_seq');
ALTER TABLE cases ALTER COLUMN id SET DEFAULT nextval('cases_id_seq');
ALTER TABLE notes ALTER COLUMN id SET DEFAULT nextval('notes_id_seq');

ALTER TABLE persons ALTER COLUMN correspondencebypost SET DEFAULT FALSE;
ALTER TABLE persons ALTER COLUMN correspondencebyphone SET DEFAULT FALSE;
ALTER TABLE persons ALTER COLUMN correspondencebyemail SET DEFAULT FALSE;

-- create a sequence for persons.uid
