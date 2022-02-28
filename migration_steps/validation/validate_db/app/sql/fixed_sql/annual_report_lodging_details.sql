-- annual_report_lodging_details

DROP TABLE IF EXISTS casrec_csv.exceptions_annual_report_lodging_details;

CREATE TABLE casrec_csv.exceptions_annual_report_lodging_details(
    caserecnumber text default NULL,
    datereportlodged text default NULL,
    bankstatementsreceived text default NULL,
    lodgedstatus text default NULL,
    lodgedby_id text default NULL,
    bankstatementdeadlinedate date default NULL,
    deadlinedate date default NULL,
    resubmitteddate date default NULL
);

INSERT INTO casrec_csv.exceptions_annual_report_lodging_details(
    SELECT
        caserecnumber as caserecnumber,
        CAST(NULLIF(datereportlodged, '') AS date) AS datereportlodged,
        casrec_csv.report_bankstatementsreceived(further_codes, rcvd_dates) AS bankstatementsreceived,
        NULLIF(COALESCE(
	        casrec_csv.report_lodged_status(
	            casrec_csv.report_lodged_status_aggregate(
	                revisedduedate, further_code, has_non_null_received_date, sent_date, follow_up_date
	            )
	        ),
        	casrec_csv.report_element(
	            casrec_csv.report_status(
	                casrec_csv.report_status_aggregate(
	                    review_status, wd_count_end_date, has_non_null_received_date, lodged_date, reviewdate, next_yr_flag
	                )
	            ), 2
	        )
        ), '') AS lodgedstatus,
        2657 as lodgedby_id,
        casrec_csv.report_bankstatementdeadlinedate(latest_further_date, last_further_code) AS bankstatementdeadlinedate,
        casrec_csv.report_deadlinedate(latest_further_date, last_further_code) AS deadlinedate,
        casrec_csv.report_resubmitteddate(further_codes, rcvd_dates) AS resubmitteddate
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
            END) AS has_non_null_received_date,
            casrec_csv.weekday_count(account."End Date") AS wd_count_end_date,
            "Revise Date" AS revisedduedate,
            "Rev Stat" AS review_status,
            "Lodge Date" AS lodged_date,
            "Review Date" AS reviewdate,
            "Next Yr" AS next_yr_flag,
            "Further Code" AS further_code,

            -- get latest date from "Further Date*" columns
            GREATEST(
                CAST(NULLIF("Further Date1", '') AS date),
                CAST(NULLIF("Further Date2", '') AS date),
                CAST(NULLIF("Further Date3", '') AS date),
                CAST(NULLIF("Further Date4", '') AS date),
                CAST(NULLIF("Further Date6", '') AS date),
                CAST(NULLIF("Further Date6.1", '') AS date)
            ) AS latest_further_date,

            -- in alphabetical order (Further1 is on left, Further6 on the right), get the last
            -- value which is not 0
            CAST(
                TO_JSON(
                    ARRAY_REMOVE(
                        ARRAY[
                            CAST(NULLIF("Further1", '') AS text),
                            CAST(NULLIF("Further2", '') AS text),
                            CAST(NULLIF("Further3", '') AS text),
                            CAST(NULLIF("Further4", '') AS text),
                            CAST(NULLIF("Further5", '') AS text),
                            CAST(NULLIF("Further6", '') AS text)
                        ],
                        '0'
                    )
                )->>-1
            AS text) AS last_further_code,

            -- all "Further*" column values
            ARRAY[
                CAST(NULLIF("Further1", '') AS text),
                CAST(NULLIF("Further2", '') AS text),
                CAST(NULLIF("Further3", '') AS text),
                CAST(NULLIF("Further4", '') AS text),
                CAST(NULLIF("Further5", '') AS text),
                CAST(NULLIF("Further6", '') AS text)
            ] AS further_codes,

            -- all "Rcvd Date*" column values
            ARRAY[
                CAST(NULLIF("Rcvd Date1", '') AS date),
                CAST(NULLIF("Rcvd Date2", '') AS date),
                CAST(NULLIF("Rcvd Date3", '') AS date),
                CAST(NULLIF("Rcvd Date4", '') AS date),
                CAST(NULLIF("Rcvd Date5", '') AS date),
                CAST(NULLIF("Rcvd Date6", '') AS date)
            ] AS rcvd_dates
        FROM casrec_csv.account
    ) AS lodge_details

    EXCEPT

    SELECT
        persons.caserecnumber AS caserecnumber,
        CAST(annual_report_lodging_details.datereportlodged AS date) AS datereportlodged,
        annual_report_lodging_details.bankstatementsreceived AS bankstatementsreceived,
        annual_report_lodging_details.lodgedstatus AS lodgedstatus,
        annual_report_lodging_details.lodgedby_id AS lodgedby_id,
        annual_report_lodging_details.bankstatementdeadlinedate,
        annual_report_lodging_details.deadlinedate,
        annual_report_lodging_details.resubmitteddate
    FROM {target_schema}.annual_report_lodging_details
    INNER JOIN {target_schema}.annual_report_logs on annual_report_logs.id = annual_report_lodging_details.annual_report_log_id
    INNER JOIN {target_schema}.persons on persons.id = annual_report_logs.client_id
);
