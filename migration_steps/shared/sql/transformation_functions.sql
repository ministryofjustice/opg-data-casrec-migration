-- NOTE
-- Add corresponding drop function in drop_transformation_functions.sql

-- capitalise
CREATE OR REPLACE FUNCTION transf_capitalise(source varchar)
RETURNS varchar AS $$
DECLARE
BEGIN
    RETURN upper(source);
END;
$$ LANGUAGE plpgsql;

-- convert_to_bool
CREATE OR REPLACE FUNCTION transf_convert_to_bool(source varchar)
RETURNS boolean AS $$
DECLARE
BEGIN
    RETURN source = '1.0';
END;
$$ LANGUAGE plpgsql;

-- money_poundPence
CREATE OR REPLACE FUNCTION transf_money_poundPence(source character)
    RETURNS decimal AS $$
DECLARE
BEGIN
    RETURN ROUND(source::numeric, 2);
END;
$$ LANGUAGE plpgsql;

-- calculate_duedate (for reporting/annual_report_logs.duedate)
CREATE OR REPLACE FUNCTION transf_calculate_duedate(source varchar)
    RETURNS date as $$
DECLARE
    DueDate date;
    DayOfWeek integer;
BEGIN
    DueDate = CAST(source AS date) + 21;

    -- if on a weekend, move to next working day
    DayOfWeek = extract(isodow from DueDate);

    IF DayOfWeek = 7 THEN
        -- Sunday
        DueDate = DueDate + 1;
    ELSIF DayOfWeek = 6 THEN
        -- Saturday
        DueDate = DueDate + 2;
    END if;

    RETURN DueDate;
END;
$$ LANGUAGE plpgsql;

-- combine date and time values to create a timestamp
CREATE OR REPLACE FUNCTION transf_convert_to_timestamp(date_part varchar, time_part varchar)
    RETURNS timestamp as $$
DECLARE
    DateVal varchar;
    TimeVal varchar;
BEGIN
    DateVal = TRIM(date_part);
    IF DateVal IN ('NaT', '') THEN
        DateVal = '1900-01-01';
    END IF;

    TimeVal = TRIM(time_part);
    IF TimeVal IN ('NaT', '') THEN
        TimeVal = '00:00:00';
    ELSE
        TimeVal = SPLIT_PART(TimeVal, '.', 1);
    END IF;

    RETURN CONCAT(DateVal, ' ', TimeVal)::timestamp;
END;
$$ LANGUAGE plpgsql;
