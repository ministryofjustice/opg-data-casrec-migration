import re

import pandas as pd
from beeprint import pp


class Mapping:
    def __init__(self, excel_doc, sheet_name):
        self.excel_doc = excel_doc
        self.sheet_name = sheet_name

    def _read_mapping_doc(self):
        sheet = pd.read_excel(io=self.excel_doc, sheet_name=self.sheet_name)

        # print(f"\n{sheet.to_markdown()}")

        return sheet

    def _apply_column_alias(self, df):

        df["count"] = df.groupby("casrec_column_name").cumcount()
        df["alias"] = df[["casrec_column_name", "count"]].values.tolist()
        df["alias"] = df["alias"].apply(
            lambda x: f"{x[0]} {x[1]}" if str(x[0]) != "nan" and int(x[1]) > 0 else x[0]
        )

        return df

    def generate_mapping_df(self):
        raw_mapping_doc = self._read_mapping_doc()
        mapping_doc_with_alias = self._apply_column_alias(df=raw_mapping_doc)

        return mapping_doc_with_alias

    def mapping_definitions(self):

        mapping_df = self.generate_mapping_df()

        interesting_columns = [
            "casrec_table",
            "casrec_column_name",
            "alias",
            "requires_transformation",
            "default_value",
            # 'is_pk',
            # 'fk_children',
            # 'fk_parents'
        ]

        # only select the columns we are interested in
        mapping_df_2 = mapping_df[interesting_columns + ["column_name"]]

        # drop any rows that have no value in all interesting cols - means they've ' \
        # 'probably not been mapped yet
        mapping_df_2 = mapping_df_2.dropna(
            axis=0, how="all", subset=interesting_columns
        )

        # fill 'nan' with empty string
        mapping_df_2 = mapping_df_2.fillna("")

        mapping_df_2 = mapping_df_2.set_index("column_name")

        mapping_definitions = mapping_df_2.to_dict("index")

        pp(mapping_definitions)

        for col, details in mapping_definitions.items():
            print(f"col: {col}")
            print(f"details: {details}")
            if "," in details["casrec_column_name"]:
                details["casrec_column_name"] = [
                    x.strip() for x in details["casrec_column_name"].split(",")
                ]
                details["alias"] = [x.strip() for x in details["alias"].split(",")]

        pp(mapping_definitions)

        return mapping_definitions


#
# def convert_to_list(columns:str) -> list:
#     if ',' in columns:
#         return columns.replace('"', '').replace(' ','').split(',')
#     else:
#         return columns
#
#
# re.sub(r"([^,\s][^\,]*[^,\s]*)", r'"\1"', x)
