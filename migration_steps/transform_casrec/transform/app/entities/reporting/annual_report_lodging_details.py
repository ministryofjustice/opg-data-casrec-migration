from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table
import logging
import os
import pandas as pd

from helpers import get_mapping_dict, get_table_def
from transform_data.apply_datatypes import apply_datatypes, reapply_datatypes_to_fk_cols

log = logging.getLogger("root")


# NB if two columns have the same value, the first one
# occurring in the list cols is used and the later ignored
# (this matches the implementation of GREATEST in SQL)
def _max_date(row: pd.Series, cols: list):
    max_col = None
    max_val = None

    for col in cols:
        if not pd.isnull(row[col]) and (max_val is None or row[col] > max_val):
            max_val = row[col]
            max_col = col

    return (
        max_val,
        max_col,
    )


# implements logic from IN-1152 and IN-1179
def _additional_dates(row: pd.Series) -> pd.Series:
    row["resubmitteddate"] = None
    row["bankstatementdeadlinedate"] = None
    row["deadlinedate"] = None
    row["bankstatementsreceived"] = None

    max_further_date, _ = _max_date(
        row,
        [
            "c_further_date1",
            "c_further_date2",
            "c_further_date3",
            "c_further_date4",
            "c_further_date6",
            "c_further_date61",
        ],
    )

    last_further_code = -1
    last_non_zero_further_col = -1

    for further_col_num in range(1, 7):
        column = f"c_further{further_col_num}"
        column_value = row[column]

        if not pd.isnull(column_value) and column_value != 0:
            last_non_zero_further_col = further_col_num
            last_further_code = column_value

    if max_further_date is not None:
        if last_further_code in [1, 8]:
            row["bankstatementdeadlinedate"] = max_further_date
        elif last_further_code in [2, 3, 4, 5, 6, 7, 99]:
            row["deadlinedate"] = max_further_date

    max_rcvd_date, rcvd_col = _max_date(
        row,
        [
            "c_rcvd_date1",
            "c_rcvd_date2",
            "c_rcvd_date3",
            "c_rcvd_date4",
            "c_rcvd_date5",
            "c_rcvd_date6",
        ],
    )

    # Check whether the c_rcvd_dateX column with latest date has the
    # same suffix as the last non-zero c_furtherY column
    # (i.e. is X == Y)
    same_index = False
    if rcvd_col is not None and max_rcvd_date is not None:
        same_index = int(rcvd_col[-1]) == last_non_zero_further_col

    if same_index:
        row["resubmitteddate"] = max_rcvd_date

    # IN-1179
    if last_further_code in [1, 8]:
        if same_index:
            row["bankstatementsreceived"] = True
        else:
            row["bankstatementsreceived"] = False

    return row


def insert_annual_report_lodging_details(db_config, target_db, mapping_file):
    chunk_size = db_config["chunk_size"]
    offset = -chunk_size
    chunk_no = 0

    mapping_file_name = f"{mapping_file}_mapping"
    table_definition = get_table_def(mapping_name=mapping_file)

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    annual_report_logs_query = f'select "id", "c_case", "End Date" from {db_config["target_schema"]}.annual_report_logs;'

    annual_report_logs = pd.read_sql_query(
        annual_report_logs_query, db_config["db_connection_string"]
    )

    while True:
        offset += chunk_size
        chunk_no += 1

        try:
            lodging_details_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            annual_report_lodging_details_joined_df = lodging_details_df.merge(
                annual_report_logs,
                how="inner",
                left_on=["c_case", "c_end_date"],
                right_on=["c_case", "End Date"],
            )

            annual_report_lodging_details_joined_df[
                "annual_report_log_id"
            ] = annual_report_lodging_details_joined_df["id_y"]
            annual_report_lodging_details_joined_df = (
                annual_report_lodging_details_joined_df.drop(columns=["id_y"])
            )
            annual_report_lodging_details_joined_df = (
                annual_report_lodging_details_joined_df.rename(columns={"id_x": "id"})
            )

            annual_report_lodging_details_joined_df = apply_datatypes(
                {
                    "c_further1": {"data_type": "int"},
                    "c_further2": {"data_type": "int"},
                    "c_further3": {"data_type": "int"},
                    "c_further4": {"data_type": "int"},
                    "c_further5": {"data_type": "int"},
                    "c_further6": {"data_type": "int"},
                    "c_further_date1": {"data_type": "date"},
                    "c_further_date2": {"data_type": "date"},
                    "c_further_date3": {"data_type": "date"},
                    "c_further_date4": {"data_type": "date"},
                    "c_further_date6": {"data_type": "date"},
                    "c_further_date61": {"data_type": "date"},
                    "c_rcvd_date1": {"data_type": "date"},
                    "c_rcvd_date2": {"data_type": "date"},
                    "c_rcvd_date3": {"data_type": "date"},
                    "c_rcvd_date4": {"data_type": "date"},
                    "c_rcvd_date5": {"data_type": "date"},
                    "c_rcvd_date6": {"data_type": "date"},
                },
                annual_report_lodging_details_joined_df,
                datetime_errors="coerce",
            )

            annual_report_lodging_details_joined_df = (
                annual_report_lodging_details_joined_df.apply(_additional_dates, axis=1)
            )

            annual_report_lodging_details_joined_df = apply_datatypes(
                {
                    "resubmitteddate": {"data_type": "date"},
                    "bankstatementdeadlinedate": {"data_type": "date"},
                    "deadlinedate": {"data_type": "date"},
                },
                annual_report_lodging_details_joined_df,
                datetime_errors="coerce",
            )

            annual_report_lodging_details_joined_df = reapply_datatypes_to_fk_cols(
                columns=["annual_report_log_id"],
                df=annual_report_lodging_details_joined_df,
            )

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=annual_report_lodging_details_joined_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

        except EmptyDataFrame as empty_data_frame:
            if empty_data_frame.empty_data_frame_type == "chunk":
                target_db.create_empty_table(
                    sirius_details=sirius_details, df=empty_data_frame.df
                )
                break
            continue
