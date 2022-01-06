import json
from datetime import datetime

import pandas as pd
from pandas.testing import assert_frame_equal

from entities.scheduled_events.scheduled_events_reporting import apply_event_column


def test_apply_event_column():
    due_by = datetime(2022, 12, 30)
    end_date = datetime(2022, 12, 31)

    test_df = pd.DataFrame(
        {
            "dueby": [due_by],
            "processed": [False],
            "version": [1],
            "client_id": [1],
            "reporting_period_id": [10],
            "end_date": [end_date],
            "event": ["{}"]
        }
    )

    expected_json = json.dumps(
        {
            "class": "Opg\\Core\\Model\\Event\\DeputyshipReporting\\ScheduledReportingPeriodEndDate",
            "payload": {
                "clientId": 1,
                "reportingPeriodId": 10,
                "endDate": "2022-12-31T00:00:00+00:00"
            }
        }
    )

    expected_df = pd.DataFrame(
        {
            "dueby": [due_by],
            "processed": [False],
            "version": [1],
            "event": [expected_json]
        }
    )

    transformed_df = apply_event_column(test_df)

    assert_frame_equal(expected_df, transformed_df)
