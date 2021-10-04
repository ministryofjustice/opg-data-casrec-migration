from utilities.standard_calculations import uuid4
import pandas as pd
import uuid


def test_uuid4():
    test_data = {
        "uuid_col": [
            "",
            "",
            "",
        ],
    }
    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    result_df = uuid4(
        column_name="uuid_col", df=test_data_df
    )

    for index, row in result_df.iterrows():
        try:
            uuid.UUID(str(row["uuid_col"]))
            assert True
        except ValueError:
            assert False
