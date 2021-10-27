from migration_steps.shared.db_helpers import (
    replace_with_sql_friendly_chars,
    replace_with_sql_friendly_chars_single,
)

input_and_expected = [
    ("nan", ""),
    ("nan ", ""),
    ("finance", "finance"),
    ("your nan", "your nan"),
    ("Nan", "Nan"),
    ("NaT", ""),
    ("NaT ", ""),
    ("Not a NaT", "Not a NaT"),
    ("<NA>", ""),
    ("<", "<"),
    ("john O'Shea", "john O''Shea"),
    ("20% awesome", "20%% awesome"),
    ("None", ""),
    ("They had None of that", "They had None of that"),
]


def test_replace_with_sql_friendly_chars():
    input_list = []
    expected_list = []
    for input_value, expected_result in input_and_expected:
        input_list.append(input_value)
        expected_list.append(expected_result)
    result_list = replace_with_sql_friendly_chars(input_list)
    assert result_list == expected_list


def test_replace_with_sql_friendly_chars_single():
    for input_value, expected_result in input_and_expected:
        result_value = replace_with_sql_friendly_chars_single(input_value)
        assert result_value == expected_result
