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
    RETURN source in ('1.0', '1');
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

-- calculate_duedate (for reporting/annual_report_logs.duedate, Lay deputies, + 21 calendar days)
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

CREATE OR REPLACE FUNCTION transf_add_business_days(in startDate date, in numDays int)
RETURNS date AS $$
    SELECT dd
    FROM (
        SELECT dd::date, row_number() OVER (ORDER BY dd ASC)
        -- numDays / 5 full weeks, plus 2 days in case we land on a weekend and have
        -- to move forward one or two days
        FROM GENERATE_SERIES(startDate + 1, startDate + 2 + ((numDays / 5) * 7), '1d') dd
        WHERE EXTRACT ('dow' from dd) NOT IN (0, 6)
    ) series
    where row_number = numDays;
$$ LANGUAGE sql;

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

    RETURN CONCAT(DateVal, ' ', TimeVal)::timestamp AT TIME ZONE 'Europe/London' AT TIME ZONE 'UTC';
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

CREATE OR REPLACE FUNCTION transf_add_one_year(source date)
RETURNS date as $$
DECLARE
BEGIN
    IF source IS NULL THEN
        RETURN NULL;
    END IF;
    RETURN source + interval '1 year';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION transf_multiply_by_100(source varchar)
RETURNS integer as $$
DECLARE
BEGIN
    RETURN (CAST(source AS DOUBLE PRECISION) * 100)::integer;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION transf_first_two_chars(source varchar)
RETURNS varchar as $$
DECLARE
BEGIN
    RETURN LEFT(source, 2);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION transf_start_of_tax_year(source date)
RETURNS timestamp as $$
DECLARE
    DateYear int;
    ThisTaxYear timestamp;
BEGIN
    DateYear = EXTRACT(YEAR FROM source)::int;
    ThisTaxYear = CONCAT(DateYear, '-04-01')::timestamp;

    IF source >= ThisTaxYear THEN
        RETURN ThisTaxYear;
    END IF;

    RETURN CONCAT(DateYear - 1, '-04-01')::timestamp;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION transf_end_of_tax_year(source date)
RETURNS timestamp as $$
DECLARE
    DateYear int;
    ThisTaxYear timestamp;
BEGIN
    DateYear = EXTRACT(YEAR FROM source)::int;
    ThisTaxYear = CONCAT(DateYear, '-04-01')::timestamp;

    IF source >= ThisTaxYear THEN
        RETURN CONCAT(DateYear + 1, '-03-31')::timestamp;
    END IF;

    RETURN CONCAT(DateYear, '-03-31')::timestamp;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION transf_fee_reduction_end_date(source date)
RETURNS date as $$
DECLARE
    DayMonth varchar;
BEGIN
    DayMonth = to_char(source, 'DD-MM');

    IF DayMonth = '31-03' THEN
        RETURN source;
    ELSIF DayMonth = '01-04' THEN
        RETURN source - INTERVAL '1 DAY';
    END IF;

    RETURN transf_end_of_tax_year(source)::date;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION transf_absolute_value(source text)
RETURNS double precision as $$
DECLARE
BEGIN
    RETURN ABS(CAST(source AS DOUBLE PRECISION));
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION transf_credit_type_from_invoice_ref(source varchar)
RETURNS varchar as $$
DECLARE
BEGIN
    IF LEFT(source, 1) = 'Z' OR RIGHT(source, 1) = 'Z' THEN
        RETURN 'CREDIT REMISSION';
    ELSIF LEFT(source, 2) = 'CR' OR RIGHT(source, 2) = 'CR' THEN
        RETURN 'CREDIT MEMO';
    ELSIF LEFT(source, 2) = 'WO' OR RIGHT(source, 2) = 'WO' THEN
        RETURN 'CREDIT WRITE OFF';
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
