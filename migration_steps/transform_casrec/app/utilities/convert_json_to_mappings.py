import logging
import os

import helpers

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


class MappingDefinitions:
    def __init__(self, mapping_definitions):
        self.mapping_definitions = mapping_definitions

    def _get_simple_mapping(self) -> dict:
        return {
            k: v
            for k, v in self.mapping_definitions.items()
            if v["casrec_column_name"] != ""
        }

    def _get_transformations(self) -> dict:
        requires_transformation = {
            k: v
            for k, v in self.mapping_definitions.items()
            if v["requires_transformation"] != ""
            and v["requires_transformation"] != "date_format_standard"
        }

        transformations = {}
        for k, v in requires_transformation.items():
            tr = v["requires_transformation"]
            d = {"original_columns": v["casrec_column_name"], "aggregate_col": k}
            if tr in transformations:
                transformations[tr].append(d)
            else:
                transformations[tr] = [d]

        return transformations

    def _get_default_values(self) -> dict:
        return {
            k: v
            for k, v in self.mapping_definitions.items()
            if v["default_value"] != "" and v["casrec_column_name"] == ""
        }

    def _get_calculations(self) -> dict:
        requires_calculation = {
            k: v for k, v in self.mapping_definitions.items() if v["calculated"] != ""
        }

        calculations = {}
        for k, v in requires_calculation.items():
            tr = v["calculated"]
            d = {"column_name": k}
            if v["calculated"] == "conditional_lookup":
                d["lookup_table"] = v["lookup_table"]
                d["original_columns"] = v["casrec_column_name"]
            if tr in calculations:
                calculations[tr].append(d)
            else:
                calculations[tr] = [d]

        return calculations

    def _get_lookup_tables(self) -> dict:
        return {
            k: v
            for k, v in self.mapping_definitions.items()
            if v["lookup_table"] != "" and v["calculated"] != "conditional_lookup"
        }

    def generate_mapping_def(self):
        return {
            "simple_mapping": self._get_simple_mapping(),
            "transformations": self._get_transformations(),
            "required_columns": self._get_default_values(),
            "calculated_fields": self._get_calculations(),
            "lookup_tables": self._get_lookup_tables(),
        }
