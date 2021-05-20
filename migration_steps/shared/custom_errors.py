import logging

log = logging.getLogger("root")


class EmptyDataFrame(Exception):
    def __init__(self, message="No data in dataframe"):
        self.message = message
        super().__init__(self.message)


class IncorrectRowCount(Exception):
    def __init__(self, message="Incorrect row count returned"):
        self.message = message
        super().__init__(self.message)
