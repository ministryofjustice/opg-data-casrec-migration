DROP TABLE IF EXISTS casrec_csv.exceptions_annual_report_logs;

CREATE TABLE casrec_csv.exceptions_annual_report_logs(
    caserecnumber text default NULL,
    reportingperiodenddate text default NULL,
    reportingperiodstartdate text default NULL,
    duedate text default NULL,
    receiveddate text default NULL,
    revisedduedate text default NULL,
    numberofchaseletters text default NULL,
    reviewdate text default NULL,
    status text default NULL,
    reviewstatus text default NULL
);

INSERT INTO casrec_csv.exceptions_annual_report_logs(
	select
	    caserecnumber,
	    CAST(reportingperiodenddate AS date) as reportingperiodenddate,
	    CAST(reportingperiodenddate AS date) - 366 AS reportingperiodstartdate,
	    duedate,
	    CAST(nullif(receiveddate, '') as date) as receiveddate,
	    CAST(nullif(revisedduedate, '') as date) as revisedduedate,
	    numberofchaseletters,
	    CAST(nullif(reviewdate, '') as date) as reviewdate,
	    casrec_csv.report_element(full_status, 1) as status,
	    casrec_csv.report_element(full_status, 3) as reviewstatus
    from (
        select
	        caserecnumber,
	        reportingperiodenddate,
	        duedate,
	        receiveddate,
	        revisedduedate,
	        numberofchaseletters,
	        reviewdate,
	        casrec_csv.report_status(
	            casrec_csv.report_status_aggregate(
	                review_status, wd_count_end_date, receiveddate, lodged_date, reviewdate, next_yr_flag
	            )
	        ) full_status
        from (
            SELECT
                "Case" as caserecnumber,
                account."End Date" AS reportingperiodenddate,
                transf_calculate_duedate(account."End Date") AS duedate,
                GREATEST(
                    NULLIF(account."Rcvd Date", ''),
                    NULLIF(account."Rcvd Date1", ''),
                    NULLIF(account."Rcvd Date2", ''),
                    NULLIF(account."Rcvd Date3", ''),
                    NULLIF(account."Rcvd Date4", ''),
                    NULLIF(account."Rcvd Date5", ''),
                    NULLIF(account."Rcvd Date6", '')
                ) AS receiveddate,
                "Revise Date" as revisedduedate,
                0 as numberofchaseletters,
                casrec_csv.weekday_count(account."End Date") as wd_count_end_date,
                "Rev Stat" as review_status,
                "Lodge Date" as lodged_date,
                "Review Date" as reviewdate,
                "Next Yr" as next_yr_flag

            FROM
                casrec_csv.account
        ) as csv_data
    ) as final_data
    except
    SELECT * FROM(
        SELECT
            persons.caserecnumber as caserecnumber,
            annual_report_logs.reportingperiodenddate AS reportingperiodenddate,
            annual_report_logs.reportingperiodstartdate AS reportingperiodstartdate,
            annual_report_logs.duedate AS duedate,
            annual_report_logs.receiveddate AS receiveddate,
            annual_report_logs.revisedduedate as revisedduedate,
            annual_report_logs.numberofchaseletters as numberofchaseletters,
            annual_report_logs.reviewdate as reviewdate,
            annual_report_logs.status,
            annual_report_logs.reviewstatus
        FROM
            annual_report_logs
            inner join persons on persons.id = annual_report_logs.client_id
        ) as sirius_data
);
