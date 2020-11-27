from pytest_cases import case


@case(id="current_date called")
def case_current_date():
    test_calculation = {
        "current_date": [{"column_name": "todays_date",},],
        "conditional_lookup": [
            {"column_name": "dateofdeath", "lookup_table": "death_lookup"},
        ],
    }

    log_message = "mock current_date"

    return (test_calculation, log_message)


# @case(id="conditional_lookup called")
# def case_conditional_lookup():
#     test_calculation = {
#         "current_date": [{"column_name": "todays_date",},],
#         "conditional_lookup": [
#             {"column_name": "dateofdeath", "lookup_table": "death_lookup"},
#         ],
#     }
#
#     log_message = "mock conditional_lookup"
#
#     return (test_calculation, log_message)
