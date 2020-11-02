import os
import logging
import colorlog as colourlog


class MyHandler(colourlog.StreamHandler):
    def __init__(self):

        colourlog.StreamHandler.__init__(self)
        fmt = "%(log_color)s %(asctime)s %(filename)-18s %(levelname)-8s: %(message)s"
        fmt_date = "%Y-%m-%dT%T%Z"

        formatter = colourlog.ColoredFormatter(
            fmt,
            fmt_date,
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
                5: "yellow",
                "VERBOSE": "yellow",
            },
            secondary_log_colors={},
            style="%",
        )

        self.setFormatter(formatter)
