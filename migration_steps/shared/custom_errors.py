import logging

log = logging.getLogger("root")


class EmptyDataFrame(Exception):
    def __init__(self, empty_data_frame_type="chunk", message="No data in dataframe", df=None):
        self.empty_data_frame_type = empty_data_frame_type
        self.message = f"{message} of type {empty_data_frame_type}"
        self.df = df
        super().__init__(self.message)


class IncorrectRowCount(Exception):
    def __init__(self, message="Incorrect row count returned"):
        self.message = message
        super().__init__(self.message)
