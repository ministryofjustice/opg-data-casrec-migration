

INSERT INTO bond_providers (id, name, oneoffvalue, telephonenumber, emailaddress, webaddress, uid)
SELECT 185, name, oneoffvalue, telephonenumber, emailaddress, webaddress, name||'_dev'
    FROM bond_providers WHERE id = 1;

INSERT INTO bond_providers (id, name, oneoffvalue, telephonenumber, emailaddress, webaddress, uid)
SELECT 186, name, oneoffvalue, telephonenumber, emailaddress, webaddress, name||'_dev'
    FROM bond_providers WHERE id = 2;

INSERT INTO bond_providers (id, name, oneoffvalue, telephonenumber, emailaddress, webaddress, uid)
SELECT 187, name, oneoffvalue, telephonenumber, emailaddress, webaddress, name||'_dev'
    FROM bond_providers WHERE id = 3;

INSERT INTO bond_providers (id, name, uid) VALUES (43745, 'OTHER', 'OTHER_dev');

