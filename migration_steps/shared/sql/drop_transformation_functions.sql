-- dropping the functions created in transformation_functions.sql

DROP FUNCTION transf_capitalise(source varchar);
DROP FUNCTION transf_convert_to_bool(source varchar);
DROP FUNCTION transf_money_poundPence(source character);
DROP FUNCTION getCasrecAddress(ad1 varchar, ad2 varchar, ad3 varchar, ad4 varchar);
DROP FUNCTION getSiriusAddress(addressLines anyelement, town varchar, county varchar);
