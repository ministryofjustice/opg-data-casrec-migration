import re

import pandas as pd


class Mapping:
    def __init__(self, excel_doc, table_definitions):
        self.excel_doc = excel_doc
        self.sheet_name = table_definitions["sheet_name"]
        self.source_table_name = table_definitions["source_table_name"]
        self.additional_columns = (
            table_definitions["source_table_additional_columns"]
            if "source_table_additional_columns" in table_definitions
            else None
        )
        self.additional_columns_list = (
            [
                {"casrec_column_name": x, "alias": f"c_{x.lower().replace(' ', '_')}"}
                for x in self.additional_columns
            ]
            if self.additional_columns
            else None
        )
        # self.limit = (
        #     config.row_limit
        #     if config.row_limit is not None
        #     else None
        # )

    def _read_mapping_doc(self):
        sheet = pd.read_excel(io=self.excel_doc, sheet_name=self.sheet_name)

        return sheet

    def _apply_column_alias(self, df):

        df["count"] = df.groupby("casrec_column_name").cumcount()
        df["alias"] = df[["casrec_column_name", "count"]].values.tolist()
        df["alias"] = df["alias"].apply(
            lambda x: f"{x[0]} {x[1]}" if str(x[0]) != "nan" and int(x[1]) > 0 else x[0]
        )

        return df

    def _apply_source_unique_id(self, df):
        df = df.append(
            {
                "column_name": "casrec_id",
                "casrec_table": self.source_table_name,
                "casrec_column_name": "rct",
                "alias": "rct",
            },
            ignore_index=True,
        )

        return df

    def simple_mapping(self, full_mapping):
        simple_mappings = full_mapping.fillna("unknown")
        simple_mappings = simple_mappings[
            simple_mappings["requires_transformation"] == "unknown"
        ]
        simple_mappings = simple_mappings[
            simple_mappings["casrec_column_name"] != "unknown"
        ]
        simple_mappings = simple_mappings[
            ["column_name", "casrec_table", "casrec_column_name", "alias"]
        ]

        simple_mappings.set_index("column_name", drop=True, inplace=True)
        simple_mappings_dict = simple_mappings.to_dict(orient="index")

        return simple_mappings_dict

    def transformation_mapping(self, full_mapping):
        transformations = full_mapping.fillna("unknown")
        transformations = transformations[
            transformations["requires_transformation"] != "unknown"
        ]
        transformations = transformations[
            [
                "column_name",
                "casrec_table",
                "casrec_column_name",
                "requires_transformation",
            ]
        ]

        transformations.set_index("column_name", drop=True, inplace=True)
        transformations_dict = transformations.to_dict(orient="index")

        t = {}
        for k, v in transformations_dict.items():
            transforamtion_name = v["requires_transformation"]
            original_columns_as_list = v["casrec_column_name"].split(",")
            cols_to_transform = {
                "original_columns": [x.strip() for x in original_columns_as_list],
                "aggregate_col": k,
            }

            if transforamtion_name in t:
                t[transforamtion_name].append(cols_to_transform)
            else:
                t[transforamtion_name] = [cols_to_transform]

        return t

    def required_columns(self, full_mapping):
        required_columns = full_mapping.fillna("unknown")
        required_columns = required_columns[required_columns["is_pk"] != True]
        required_columns = required_columns[required_columns["nullable"] == False]
        required_columns = required_columns[required_columns["autoincrement"] == False]
        required_columns = required_columns[
            required_columns["requires_transformation"] == "unknown"
        ]
        required_columns = required_columns[
            required_columns["casrec_column_name"] == "unknown"
        ]
        required_columns = required_columns[required_columns["default"] == "unknown"]
        required_columns = required_columns[
            ["column_name", "data_type", "default_value"]
        ]
        required_columns.set_index("column_name", drop=True, inplace=True)
        required_columns_dict = required_columns.to_dict(orient="index")

        return required_columns_dict

    def generate_mapping_df(self):
        raw_mapping_doc = self._read_mapping_doc()
        mapping_doc_with_alias = self._apply_column_alias(df=raw_mapping_doc)
        mapping_doc_with_unique_id = self._apply_source_unique_id(
            df=mapping_doc_with_alias
        )

        return mapping_doc_with_unique_id

    def mapping_definitions(self):

        mapping_df = self.generate_mapping_df()

        mapping_definitions = {}
        mapping_definitions["simple_mapping"] = self.simple_mapping(
            full_mapping=mapping_df
        )
        mapping_definitions["transformations"] = self.transformation_mapping(
            full_mapping=mapping_df
        )
        mapping_definitions["required_columns"] = self.required_columns(
            full_mapping=mapping_df
        )

        return mapping_definitions

    def generate_select_string_from_mapping(self):
        mapping = self.generate_mapping_df()

        cols = mapping[mapping["casrec_column_name"].notna()]

        cols = cols[cols["casrec_table"].str.lower() == self.source_table_name][
            ["casrec_column_name", "alias"]
        ]

        col_names_with_alias = cols.to_dict(orient="records")
        if self.additional_columns_list:
            col_names_with_alias = col_names_with_alias + self.additional_columns_list

        statement = "SELECT "
        for i, col in enumerate(col_names_with_alias):
            if "," in col["casrec_column_name"]:
                # split comma separated list of cols
                # eg "Dep Adrs1,Dep Adrs2,Dep Adrs3"
                statement += re.sub(
                    r"([^,\s][^\,]*[^,\s]*)", r'"\1"', col["casrec_column_name"]
                )
            else:
                statement += f"\"{col['casrec_column_name']}\" as \"{col['alias']}\""
            if i + 1 < len(col_names_with_alias):
                statement += ", "
            else:
                statement += " "
        statement += f"FROM etl1.{self.source_table_name} "
        # if self.limit:
        #     statement += f"LIMIT {self.limit}"
        return f"{statement};"
