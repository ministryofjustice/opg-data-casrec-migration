-- annual_report_lodging_details

DROP TABLE IF EXISTS casrec_csv.exceptions_annual_report_lodging_details;

CREATE TABLE casrec_csv.exceptions_annual_report_lodging_details(
    caserecnumber text default NULL,
    deadlinedate text default NULL,
    datereportlodged text default NULL,
    bankstatementdeadlinedate text default NULL,
    bankstatementsreceived text default NULL,
    lodgedstatus text default NULL,
    lodgedby_id text default NULL
);

INSERT INTO casrec_csv.exceptions_annual_report_lodging_details(
    SELECT
        caserecnumber as caserecnumber,
        CAST(NULLIF(follow_up_date, '') AS date) AS deadlinedate,
        CAST(NULLIF(datereportlodged, '') AS date) AS datereportlodged,
        sent_date AS bankstatementdeadlinedate,
        CASE
        	WHEN bankstatementsreceived = 'Y' THEN TRUE
        	ELSE FALSE
        end AS bankstatementsreceived,
        NULLIF(COALESCE(
	        casrec_csv.report_lodged_status(
	            casrec_csv.report_lodged_status_aggregate(
	                revisedduedate, further_code, bankstatementsreceived, sent_date, follow_up_date
	            )
	        ),
        	casrec_csv.report_element(
	            casrec_csv.report_status(
	                casrec_csv.report_status_aggregate(
	                    review_status, wd_count_end_date, bankstatementsreceived, lodged_date, reviewdate, next_yr_flag
	                )
	            ), 2
	        )
        ), '') AS lodgedstatus,
        2657 as lodgedby_id
    FROM (
        SELECT
            "Case" AS caserecnumber,
            account."Followup Date" AS follow_up_date,
            account."Lodge Date" AS datereportlodged,
            GREATEST(
                CAST(NULLIF(account."Sent1", '') AS date),
                CAST(NULLIF(account."Sent2", '') AS date),
                CAST(NULLIF(account."Sent3", '') AS date),
                CAST(NULLIF(account."Sent4", '') AS date),
                CAST(NULLIF(account."Sent5", '') AS date),
                CAST(NULLIF(account."Sent6", '') AS date)
            ) AS sent_date,
            (CASE
                WHEN (
                    (account."Rcvd Date" != '') OR
                    (account."Rcvd Date1" != '') OR
                    (account."Rcvd Date2" != '') OR
                    (account."Rcvd Date3" != '') OR
                    (account."Rcvd Date4" != '') OR
                    (account."Rcvd Date5" != '') OR
                    (account."Rcvd Date6" != '')
                )
                THEN 'Y'
                ELSE ''
            END) AS bankstatementsreceived,
            casrec_csv.weekday_count(account."End Date") AS wd_count_end_date,
            "Revise Date" AS revisedduedate,
            "Rev Stat" AS review_status,
            "Lodge Date" AS lodged_date,
            "Review Date" AS reviewdate,
            "Next Yr" AS next_yr_flag,
            "Further Code" AS further_code
        FROM casrec_csv.account
    ) AS lodge_details
    EXCEPT
    SELECT
        persons.caserecnumber AS caserecnumber,
        CAST(annual_report_lodging_details.deadlinedate AS date) AS deadlinedate,
        CAST(annual_report_lodging_details.datereportlodged AS date) AS datereportlodged,
        CAST(annual_report_lodging_details.bankstatementdeadlinedate AS date) AS bankstatementdeadlinedate,
        annual_report_lodging_details.bankstatementsreceived AS bankstatementsreceived,
        annual_report_lodging_details.lodgedstatus AS lodgedstatus,
        annual_report_lodging_details.lodgedby_id AS lodgedby_id
    FROM {target_schema}.annual_report_lodging_details
    INNER JOIN {target_schema}.annual_report_logs on annual_report_logs.id = annual_report_lodging_details.annual_report_log_id
    INNER JOIN {target_schema}.persons on persons.id = annual_report_logs.client_id
);
