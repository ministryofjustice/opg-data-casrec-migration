CREATE OR REPLACE FUNCTION {casrec_mapping}.transf_add_business_days(in startDate date, in numDays int)
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

-- calculate_duedate (for reporting/annual_report_logs.duedate, Lay deputies = + 21 calendar days,
-- moving to next working day if on a weekend)
CREATE OR REPLACE FUNCTION {casrec_mapping}.transf_calculate_duedate(in source date)
    RETURNS date as $$
DECLARE
    DueDate date;
    DayOfWeek integer;
BEGIN
    DueDate = source + INTERVAL '21 days';

    -- if on a weekend, move to next working day
    DayOfWeek = extract(isodow from DueDate);

    IF DayOfWeek = 7 THEN
        -- Sunday
        DueDate = DueDate + INTERVAL '1 day';
    ELSIF DayOfWeek = 6 THEN
        -- Saturday
        DueDate = DueDate + INTERVAL '2 days';
    END IF;

    RETURN DueDate;
END;
$$ LANGUAGE plpgsql;