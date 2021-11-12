import logging

log = logging.getLogger("root")


class EmptyDataFrame(Exception):
    def __init__(self, message="No data in dataframe"):
        """
        TODO: believe this may be deprecated and can be removed

        df: empty dataframe which caused the exception; retained so
            we can access its column metadata
        """
        self.message = message
        super().__init__(self.message)
