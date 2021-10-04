import logging
import os
import uuid
from datetime import datetime

import helpers
import pandas as pd

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def current_date(column_name: str, df: pd.DataFrame) -> pd.DataFrame:
    df[column_name] = datetime.now().strftime("%Y-%m-%d")

    return df


def uuid4(column_name: str, df: pd.DataFrame) -> pd.DataFrame:
    df[column_name] = df.apply(lambda x: uuid.uuid4(), axis=1)

    return df
