import json
from typing import List, Dict
import os
import pandas as pd


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
            # 'is_pk',
            # 'fk_children',
            # 'fk_parents'
        ]
        self.columns = columns if len(columns) > 0 else self.default_columns

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
        1. add the 'alias' col to the dataframe
        2. only select the columns we are interested in
        3. drop any rows that have no value in all interesting cols - means they've
            probably not been mapped yet
        4. fill 'nan' with empty string
        5. set index
        6. convert to dictionary
        """

        mapping_df = self._apply_column_alias(df=df)
        mapping_df = mapping_df[self.columns + [self.index_column]]
        mapping_df = mapping_df.dropna(axis=0, how="all", subset=self.columns)
        mapping_df = mapping_df.fillna("")
        mapping_df = mapping_df.set_index(self.index_column)
        mapping_dict = mapping_df.to_dict("index")

        return mapping_dict

    def _format_multiple_columns(self, mapping_dict: Dict):
        """
        Some items are across multiple columns in the source data but map to a single
        column in the destination.
        These come out of Excel as a string, we need to convert them to a list.
        Easier to do it once it's a dict than in the dataframe, as the numpy concept of
        'list' doesn't map easily using 'to_dict'!
        """

        for col, details in mapping_dict.items():
            if "," in details[self.source_column_name]:
                details[self.source_column_name] = [
                    x.strip() for x in details[self.source_column_name].split(",")
                ]
                details["alias"] = [x.strip() for x in details["alias"].split(",")]

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

    def generate_json_files(self):

        all_modules = self.get_sheets_as_dataframes()

        for module in all_modules:
            for name, df in module.items():
                module_dict = self._clean_up_and_convert_to_dict(df=df)
                if len(module_dict) > 0:
                    module_dict = self._format_multiple_columns(
                        mapping_dict=module_dict
                    )

                    self.export_single_module_as_json_file(
                        module_name=name, mapping_dict=module_dict
                    )
