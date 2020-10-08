import pandas as pd


class Mapping:
    def _read_mapping_doc(self, file_name, sheet_name):
        sheet = pd.read_excel(io=file_name, sheet_name=sheet_name)

        return sheet

    def _apply_column_alias(self, df):
        df["count"] = df.groupby("casrec_column_name").cumcount()
        df["alias"] = df[["casrec_column_name", "count"]].values.tolist()
        df["alias"] = df["alias"].apply(
            lambda x: f"{x[0]} {x[1]}" if str(x[0]) != "nan" and int(x[1]) > 0 else x[0]
        )

        return df

    def _apply_source_unique_id(self, df, source_table_name):
        df = df.append(
            {
                "column_name": "casrec_id",
                "casrec_table": source_table_name,
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

    def mapping_df(self, file_name, sheet_name, source_table_name):
        mapping_doc = self._read_mapping_doc(file_name=file_name, sheet_name=sheet_name)
        mapping_doc = self._apply_column_alias(df=mapping_doc)
        mapping_doc = self._apply_source_unique_id(
            df=mapping_doc, source_table_name=source_table_name
        )

        return mapping_doc

    def mapping_definitions(self, mapping_df):

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
