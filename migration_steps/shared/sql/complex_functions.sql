DROP TABLE IF EXISTS casrec_csv.working_day_calendar;

SELECT dd INTO casrec_csv.working_day_calendar
FROM
(SELECT dd, extract(DOW FROM dd) dw
FROM generate_series((now() - INTERVAL '1 YEAR')::date, now()::date, '1 day'::interval) dd) d
WHERE dw not in (6,0);

CREATE OR REPLACE FUNCTION casrec_csv.report_status_aggregate(rev_stat varchar, weekdays_since int, rcvd_date varchar, lodge_date varchar, review_date varchar, next_year varchar)
RETURNS
	varchar AS $$
DECLARE
	report_status_code varchar;
	end_date_flag varchar;
	rcvd_date_flag varchar;
	lodge_date_flag varchar;
	review_date_flag varchar;
	next_year_flag varchar;
BEGIN
	end_date_flag = CASE
		WHEN weekdays_since BETWEEN 1 AND 15 THEN 'F0'
		WHEN weekdays_since BETWEEN 16 AND 71 THEN 'F1'
		WHEN weekdays_since > 71 THEN 'F2'
		ELSE 'P0'
	END;
	-- lodge date is used to set rcvd_date if rcvd_date is empty; see IN-1088
	rcvd_date_flag = CASE
		WHEN COALESCE(rcvd_date, lodge_date, '') = '' THEN 'N'
		ELSE 'Y'
	END;
	lodge_date_flag = CASE
		WHEN COALESCE(lodge_date, '') = '' THEN 'N'
		ELSE 'Y'
	END;
	review_date_flag = CASE
		WHEN COALESCE(review_date, '') = '' THEN 'N'
		ELSE 'Y'
	END;
	next_year_flag = CASE
		WHEN next_year = 'Y' THEN 'Y'
		ELSE 'N'
	END;
	report_status_code = concat(rev_stat, '_', end_date_flag, '_', rcvd_date_flag, '_', lodge_date_flag, '_', review_date_flag, '_', next_year_flag);
RETURN report_status_code;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION casrec_csv.report_lodged_status_aggregate(revise_date varchar, further_code varchar, rcvd_date varchar, sent date, followup_date varchar)
RETURNS
	varchar AS $$
DECLARE
    report_lodged_status_code varchar;
	revise_date_flag varchar;
	further_code_flag varchar;
	rcvd_date_flag varchar;
	sent_flag varchar;
	followup_date_flag varchar;
BEGIN
	revise_date_flag = CASE
		WHEN COALESCE(revise_date, '') = '' THEN 'N'
		ELSE 'Y'
	END;
	further_code_flag = CASE
		WHEN further_code = '2' THEN 'A'
		WHEN further_code = '3' THEN 'A'
		WHEN further_code = '4' THEN 'A'
		WHEN further_code = '1' THEN 'B'
		WHEN further_code = '8' THEN 'B'
		when further_code = '' then 'N'
		ELSE 'X'
	END;
	rcvd_date_flag = CASE
		WHEN COALESCE(rcvd_date, '') = '' THEN 'N'
		ELSE 'Y'
	END;
	sent_flag = CASE
		WHEN sent IS NULL THEN 'N'
		ELSE 'Y'
	END;
    followup_date_flag = CASE
		WHEN COALESCE(followup_date, '') = '' THEN 'N'
		ELSE 'Y'
	END;
	report_lodged_status_code = concat(revise_date_flag, '_', further_code_flag, '_', rcvd_date_flag, '_', sent_flag, '_', followup_date_flag);
RETURN report_lodged_status_code;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION casrec_csv.report_status(report_aggr_code varchar)
RETURNS
	varchar AS $$
DECLARE
	report_status varchar;
BEGIN
	report_status = CASE
		WHEN report_aggr_code like 'N_P0_N_N_N_%' THEN 'PENDING||NO_REVIEW'
		WHEN report_aggr_code like 'N_F0_N_N_N_%' THEN 'DUE||NO_REVIEW'
		WHEN report_aggr_code like 'N_F1_N_N_N_%' THEN 'OVERDUE||NO_REVIEW'
		WHEN report_aggr_code like 'N_F2_N_N_N_%' THEN 'NON_COMPLIANT||NO_REVIEW'
		WHEN report_aggr_code like 'N_%_Y_N_N_%' THEN 'RECEIVED||NO_REVIEW'
		WHEN report_aggr_code like 'N_%_Y_Y_N_%' THEN 'LODGED|ACKNOWLEDGED|NO_REVIEW'
		WHEN report_aggr_code like 'N_%_Y_Y_Y_%' THEN 'LODGED||'
		WHEN report_aggr_code like 'I_%_Y_Y_N_%' THEN 'INCOMPLETE|INCOMPLETE|NO_REVIEW'
		WHEN report_aggr_code like 'I_%_Y_Y_Y_%' THEN 'INCOMPLETE||NO_REVIEW'
		WHEN report_aggr_code like 'S_%_Y_N_N_%' THEN 'DUE||STAFF_REFERRED'
		WHEN report_aggr_code like 'S_%_Y_Y_N_%' THEN 'LODGED|REFERRED_FOR_REVIEW|STAFF_REFERRED'
		WHEN report_aggr_code like 'S_%_Y_Y_Y_%' THEN 'LODGED|REFERRED_FOR_REVIEW|REVIEWED'
		WHEN report_aggr_code like 'S_%_N_N_%_%' THEN 'OVERDUE||'
		WHEN report_aggr_code like 'R_%_N_N_N_%' THEN 'OVERDUE||'
		WHEN report_aggr_code like 'R_%_Y_N_N_%' THEN 'DUE||STAFF_REFERRED'
		WHEN report_aggr_code like 'R_%_Y_Y_N_%' THEN 'OVERDUE||'
		WHEN report_aggr_code like 'R_%_Y_Y_Y_%' THEN 'LODGED|REFERRED_FOR_REVIEW|REVIEWED'
		WHEN report_aggr_code like 'G_%_Y_Y_N_%' THEN 'LODGED||STAFF_REFERRED'
		WHEN report_aggr_code like 'G_%_Y_Y_Y_%' THEN 'LODGED|REFERRED_FOR_REVIEW|REVIEWED'
		WHEN report_aggr_code like 'M_%_Y_Y_Y_%' THEN 'LODGED|REFERRED_FOR_REVIEW|REVIEWED'
		WHEN report_aggr_code like 'X_%_%_%_%_%' THEN 'ABANDONED||NO_REVIEW'
		WHEN report_aggr_code like '%_P0_%_%_N_Y' THEN 'PENDING||STAFF_PRESELECTED'
		ELSE NULL
	END;
RETURN report_status;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION casrec_csv.report_lodged_status(report_lodged_aggr_code varchar)
RETURNS
	varchar AS $$
DECLARE
	report_lodged_status varchar;
BEGIN
	report_lodged_status = CASE
		WHEN report_lodged_aggr_code = 'Y_A_N_N_Y' THEN 'INCOMPLETE'
		WHEN report_lodged_aggr_code = 'Y_A_Y_N_Y' THEN 'INCOMPLETE'
		WHEN report_lodged_aggr_code = 'Y_B_N_Y_N' THEN 'REFERRED_FOR_REVIEW'
		WHEN report_lodged_aggr_code = 'Y_B_Y_Y_N' THEN 'REFERRED_FOR_REVIEW'
        WHEN report_lodged_aggr_code = 'N_N_N_N_N' THEN 'REFERRED_FOR_REVIEW'
		ELSE NULL
	END;
RETURN report_lodged_status;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION casrec_csv.report_element(full_string varchar, element_no int)
RETURNS
	varchar AS $$
DECLARE
	code_part varchar;
BEGIN
	code_part = split_part(full_string, '|', element_no);
RETURN code_part;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION casrec_csv.weekday_count(string_date varchar)
RETURNS
	int AS $$
DECLARE
	weekday_count int;
BEGIN
weekday_count = count(*)
FROM casrec_csv.working_day_calendar
WHERE cast(string_date AS date) <= dd;
RETURN weekday_count;
end;
$$ LANGUAGE plpgsql;
