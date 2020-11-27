# from utilities.standard_calculations import conditional_lookup
# import pandas as pd
#
#
# def test_conditional_lookup(mock_get_lookup_dict_conditional):
#
#     column_name = "dateofdeath"
#     lookup_file_name = "death_lookup"
#     casrec_column_name = "Term Date"
#
#     test_data = {
#         "dateofdeath": ["D", "E", ""],
#     }
#
#     test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])
#
#     result = conditional_lookup(
#         column_name, casrec_column_name, lookup_file_name, test_data_df
#     )
#
#     print(result)
#
#     pass
