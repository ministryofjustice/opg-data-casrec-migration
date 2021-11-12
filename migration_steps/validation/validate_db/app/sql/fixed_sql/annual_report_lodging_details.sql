-- annual_report_lodging_details
DROP TABLE IF EXISTS casrec_csv.exceptions_annual_report_lodging_details;

CREATE TABLE casrec_csv.exceptions_annual_report_lodging_details(
    deadlinedate text default NULL,
    datereportlodged text default NULL,
    lodgedstatus text default NULL,
    bankstatementdeadlinedate text default NULL,
    bankstatementsreceived text default NULL
);

INSERT INTO casrec_csv.exceptions_annual_report_lodging_details(
    SELECT
        CAST(NULLIF(account."Followup Date", '') AS date) AS deadlinedate,
        CAST(NULLIF(account."Lodge Date", '') AS date) AS datereportlodged,
        NULLIF(TRIM(casrec_csv.furthered_lookup(account."Further Code")), '') AS lodgedstatus,
        GREATEST(
            CAST(NULLIF(account."Sent1", '') AS date),
            CAST(NULLIF(account."Sent2", '') AS date),
            CAST(NULLIF(account."Sent3", '') AS date),
            CAST(NULLIF(account."Sent4", '') AS date),
            CAST(NULLIF(account."Sent5", '') AS date),
            CAST(NULLIF(account."Sent6", '') AS date)
        ) AS bankstatementdeadlinedate,
        (CASE
            WHEN (
                (account."Rcvd Date1" != '') OR
                (account."Rcvd Date2" != '') OR
                (account."Rcvd Date3" != '') OR
                (account."Rcvd Date4" != '') OR
                (account."Rcvd Date5" != '') OR
                (account."Rcvd Date6" != '')
            )
            THEN TRUE
            ELSE FALSE
        END) AS bankstatementsreceived
    FROM casrec_csv.account

    EXCEPT

    SELECT
        CAST(annual_report_lodging_details.deadlinedate AS date) AS deadlinedate,
        CAST(annual_report_lodging_details.datereportlodged AS date) AS datereportlodged,
        NULLIF(TRIM(annual_report_lodging_details.lodgedstatus), '') AS lodgedstatus,
        CAST(annual_report_lodging_details.bankstatementdeadlinedate AS date) AS bankstatementdeadlinedate,
        annual_report_lodging_details.bankstatementsreceived AS bankstatementsreceived
    FROM {target_schema}.annual_report_lodging_details
);