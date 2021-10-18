import logging

log = logging.getLogger("root")


class EmptyDataFrame(Exception):
    def __init__(self, message="No data in dataframe"):
        """
        TODO: believe this may be deprecated and can be removed
        """
        self.message = message
        super().__init__(self.message)
