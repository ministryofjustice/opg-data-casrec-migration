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
CREATE OR REPLACE FUNCTION transf_convert_to_timestamp(date_part varchar, time_part varchar, default_date varchar)
    RETURNS timestamp as $$
DECLARE
    DateVal varchar;
    TimeVal varchar;
BEGIN
    DateVal = TRIM(date_part);
    IF DateVal IN ('NaT', '') THEN
        DateVal = default_date;
    END IF;

    IF DateVal IS NULL THEN
        RETURN NULL;
    END IF;

    DateVal = DateVal::date::varchar;

    TimeVal = TRIM(time_part);
    IF TimeVal IN ('NaT', '') THEN
        TimeVal = '00:00:00';
    ELSE
        TimeVal = SPLIT_PART(TimeVal, '.', 1);
    END IF;

    TimeVal = TimeVal::time::varchar;

    RETURN CONCAT(DateVal, ' ', TimeVal)::timestamp;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION transf_first_word(source varchar)
RETURNS varchar as $$
DECLARE
BEGIN
RETURN INITCAP(split_part(source, ' ', 1));
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION transf_last_words(source varchar)
RETURNS varchar as $$
DECLARE
BEGIN
RETURN INITCAP(COALESCE(SUBSTRING(source FROM ' .*$'), ''));
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION transf_capitalise_first_letter(source varchar)
RETURNS varchar as $$
DECLARE
BEGIN
RETURN INITCAP(source);
END;
$$ LANGUAGE plpgsql;
