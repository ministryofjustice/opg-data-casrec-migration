from datetime import datetime
import json
from typing import List, Dict
import os
import pandas as pd
from deepdiff import DeepDiff

pd.options.mode.chained_assignment = None


class Mapping:
    def __init__(self, excel_doc: str, output_folder: str, columns: List[str] = []):
        self.excel_doc = excel_doc
        self.index_column = "column_name"
        self.source_column_name = "casrec_column_name"
        self.json_path = output_folder
        self.default_columns = [
            "casrec_table",
            "casrec_column_name",
            "alias",
            "requires_transformation",
            "default_value",
            "calculated",
            "is_pk",
            # 'fk_children',
            "fk_parents",
            "is_complete",
        ]
        self.columns = columns if len(columns) > 0 else self.default_columns
        self.diff = {
            "generated_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "previous_generate_date": "",
        }
        self.summary = {
            "worksheets": {},
            "total": {
                "worksheets": {"total_sheets": 0, "total_complete": 0,},
                "fields": {
                    "total_fields": 0,
                    "total_unmapped": 0,
                    "total_mapped": 0,
                    "percentage_complete": 0,
                },
            },
        }

    def _apply_column_alias(self, df):
        """
        Some source columns are used multiple times when mapping to the destination.
        This appends a number to the column alias for the duplicates, makes the
        transformations easier as some of the duplicates are handled differently
        """

        df["count"] = df.groupby(self.source_column_name).cumcount()
        df["alias"] = df[[self.source_column_name, "count"]].values.tolist()
        df["alias"] = df["alias"].apply(
            lambda x: f"{x[0]} {x[1]}" if str(x[0]) != "nan" and int(x[1]) > 0 else x[0]
        )

        return df

    def _clean_up_and_convert_to_dict(self, df: pd.DataFrame) -> Dict:
        """
        1.  add the 'alias' col to the dataframe
        2.  only select the columns we are interested in
        3.  remove False from 'is_pk' col
        4.  convert 'is_complete' rows to boolean: True
        5.  convert 'is_complete' rows to boolean: False
        6.  drop any rows that have no value in all interesting cols
        7.  fill 'nan' with empty string
        8.  set 'include' to True where 'is_complete' is not N/A (ie, means it should
            be mapped even if the mapping is not complete)
        9.  force pk fields to be included
        10. force fk link fields to be included
        11. only select the rows where 'include' is True
        12. drop the include col (because it's always True)
        13. set index to the column name so the to_dict pivots on the sirius column name
        14. convert to dictionary
        """

        # add the 'alias' col to the dataframe
        mapping_df = self._apply_column_alias(df=df)
        # only select the columns we are interested in
        mapping_df = mapping_df[self.columns + [self.index_column]]
        # remove False from 'is_pk' col
        mapping_df["is_pk"] = mapping_df.apply(
            lambda x: True if x["is_pk"] is True else "", axis=1
        )
        # convert 'is_complete' rows to boolean: True
        mapping_df["is_complete"] = mapping_df.apply(
            lambda x: True if x["is_complete"] in ["yes", "YES"] else x["is_complete"],
            axis=1,
        )
        # convert 'is_complete' rows to boolean: False
        mapping_df["is_complete"] = mapping_df.apply(
            lambda x: False if x["is_complete"] in ["no", "NO"] else x["is_complete"],
            axis=1,
        )
        # drop any rows that have no value in all interesting cols
        mapping_df = mapping_df.dropna(axis=0, how="all", subset=self.columns)
        # fill 'nan' with empty string
        mapping_df = mapping_df.fillna("")
        # set 'include' to True where 'is_complete' is not N/A (ie, means it should be
        # mapped even if the mapping is not complete)
        mapping_df["include"] = mapping_df.apply(
            lambda x: True if x["is_complete"] != "" else False, axis=1
        )
        # force pk fields to be included
        mapping_df["include"] = mapping_df.apply(
            lambda x: True if x["is_pk"] is True else x["include"], axis=1
        )
        # force fk link fields to be included
        mapping_df["include"] = mapping_df.apply(
            lambda x: True if x["fk_parents"] != "" else x["include"], axis=1
        )
        # only select the rows where include is True
        mapping_df = mapping_df.loc[mapping_df["include"] == True]
        # drop the include col (because it's always True)
        mapping_df.drop("include", axis=1, inplace=True)
        # print(mapping_df.to_markdown())
        # set index to the column name so the to_dict pivots on the sirius column name
        mapping_df = mapping_df.set_index(self.index_column)
        # convert to dictionary
        mapping_dict = mapping_df.to_dict("index")

        return mapping_dict

    def _add_single_module_details_to_summary(self, name, mapping_dict):

        module_total_rows = len(mapping_dict)
        module_total_unmapped_rows = len(
            [k for k, v in mapping_dict.items() if v["is_complete"] is False]
        )
        module_total_mapped_rows = module_total_rows - module_total_unmapped_rows
        module_percentage_complete = round(
            module_total_mapped_rows / module_total_rows * 100
        )

        self.summary["worksheets"][name] = {}
        self.summary["worksheets"][name]["total_rows"] = module_total_rows
        self.summary["worksheets"][name]["total_unmapped"] = module_total_unmapped_rows
        self.summary["worksheets"][name]["total_mapped"] = module_total_mapped_rows
        self.summary["worksheets"][name][
            "percentage_complete"
        ] = module_percentage_complete

        fields = self.summary["total"]["fields"]
        sheets = self.summary["total"]["worksheets"]

        fields["total_fields"] += module_total_rows
        fields["total_unmapped"] += module_total_unmapped_rows
        fields["total_mapped"] += module_total_mapped_rows
        fields["percentage_complete"] = round(
            fields["total_mapped"] / fields["total_fields"] * 100
        )

        sheets["total_sheets"] += 1
        sheets["total_complete"] = (
            sheets["total_complete"] + 1 if module_percentage_complete == 100 else +0
        )

    def _format_multiple_columns(self, mapping_dict: Dict):
        """
        Some items are across multiple columns in the source data but map to a single
        column in the destination.
        These come out of Excel as a string, we need to convert them to a list.
        Easier to do it once it's a dict than in the dataframe, as the numpy concept of
        'list' doesn't map easily using 'to_dict'!
        """

        for col, details in mapping_dict.items():
            if "\n" in details[self.source_column_name]:
                details[self.source_column_name] = [
                    x.strip() for x in details[self.source_column_name].split("\n")
                ]
                details["alias"] = [x.strip() for x in details["alias"].split("\n")]

        return mapping_dict

    def _convert_sheet_name_to_module_name(self, sheet_name: str):
        """
        Excel sheet names are for humans.
        """
        return sheet_name.replace(" ", "_").replace("(", "").replace(")", "").lower()

    def get_sheets_as_dataframes(self) -> List[Dict[str, pd.DataFrame]]:
        """
        We need to process each sheet individually
        """

        excel_df = pd.ExcelFile(self.excel_doc)

        all_sheets = [
            {
                self._convert_sheet_name_to_module_name(sheet): pd.read_excel(
                    excel_df, sheet_name=sheet
                )
            }
            for sheet in excel_df.sheet_names
        ]

        return all_sheets

    def export_single_module_as_json_file(self, module_name, mapping_dict):

        if not os.path.exists(self.json_path):
            os.makedirs(self.json_path)

        with open(f"{self.json_path}/{module_name}_mapping.json", "w") as json_out:
            json.dump(mapping_dict, json_out, indent=4)

    def export_summary_as_json_file(self):

        path = f"{self.json_path}/meta"

        if not os.path.exists(path):
            os.makedirs(path)

        with open(f"{path}/mapping_progress_summary.json", "w") as json_out:
            json.dump(self.summary, json_out, indent=4)

    def generate_diff_for_module(self, module_name, module_dict):
        try:
            with open(
                f"{self.json_path}/{module_name}_mapping.json", "r"
            ) as original_file:
                original_data = original_file.read()
                original_dict = json.loads(original_data)
                diff = DeepDiff(original_dict, module_dict)

                self.diff[module_name] = diff
        except Exception:
            pass

        try:
            with open(f"{self.json_path}/meta/diff.json", "r") as previous_diff:
                diff = previous_diff.read()
                diff_dict = json.loads(diff)
                previous_date = diff_dict["generated_date"]
                self.diff["previous_generate_date"] = previous_date
        except Exception:
            pass

    def export_diff_as_json_file(self):

        path = f"{self.json_path}/meta"

        if not os.path.exists(path):
            os.makedirs(path)

        with open(f"{path}/diff.json", "w") as json_out:
            json.dump(self.diff, json_out, indent=4)

    def generate_json_files(self):

        all_modules = self.get_sheets_as_dataframes()

        for module in all_modules:
            for name, df in module.items():
                # if "_lookup" not in name:
                if name in ["client_persons", "client_addresses"]:
                    module_dict = self._clean_up_and_convert_to_dict(df=df)

                    self._add_single_module_details_to_summary(
                        name=name, mapping_dict=module_dict
                    )
                    if len(module_dict) > 0:
                        module_dict = self._format_multiple_columns(
                            mapping_dict=module_dict
                        )

                        self.generate_diff_for_module(
                            module_name=name, module_dict=module_dict
                        )

                        self.export_single_module_as_json_file(
                            module_name=name, mapping_dict=module_dict
                        )
        self.export_summary_as_json_file()
        self.export_diff_as_json_file()
