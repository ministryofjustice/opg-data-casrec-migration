-- dropping the functions created in transformation_functions.sql

DROP FUNCTION transf_capitalise(source varchar);
DROP FUNCTION transf_convert_to_bool(source varchar);
DROP FUNCTION transf_money_poundPence(source character);
DROP FUNCTION transf_calculate_duedate(source varchar);
DROP FUNCTION transf_convert_to_timestamp(date_part varchar, time_part varchar, default_date varchar);