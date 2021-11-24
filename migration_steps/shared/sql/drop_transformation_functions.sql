-- dropping the functions created in transformation_functions.sql

DROP FUNCTION transf_capitalise(source varchar);
DROP FUNCTION transf_convert_to_bool(source varchar);
DROP FUNCTION transf_money_poundPence(source character);
DROP FUNCTION transf_calculate_duedate(source varchar);
DROP FUNCTION transf_convert_to_timestamp(date_part varchar, time_part varchar, default_date varchar);
DROP FUNCTION transf_add_one_year(source date);
DROP FUNCTION transf_multiply_by_100(source varchar);
DROP FUNCTION transf_first_two_chars(source varchar);
DROP FUNCTION transf_start_of_tax_year(source date);
DROP FUNCTION transf_end_of_tax_year(source date);
DROP FUNCTION transf_fee_reduction_end_date(source date);
