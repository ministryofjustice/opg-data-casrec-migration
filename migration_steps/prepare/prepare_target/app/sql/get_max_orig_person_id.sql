SELECT MAX(id) FROM persons WHERE coalesce(clientsource, '') NOT IN ('SKELETON', 'CASRECMIGRATION')
