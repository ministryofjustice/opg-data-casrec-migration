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
                "CRITICAL": "black,bg_green",
                "VERBOSE": "yellow",
                "DATA": "red",
            },
            secondary_log_colors={},
            style="%",
        )

        self.setFormatter(formatter)


def custom_log_level(levels):

    logging.VERBOSE = levels["VERBOSE"]
    logging.addLevelName(logging.VERBOSE, "VERBOSE")
    logging.Logger.verbose = lambda inst, msg, *args, **kwargs: inst.log(
        logging.VERBOSE, msg, *args, **kwargs
    )

    logging.DATA = levels["DATA"]
    logging.addLevelName(logging.DATA, "DATA")
    logging.Logger.data = lambda inst, msg, *args, **kwargs: inst.log(
        logging.DATA, msg, *args, **kwargs
    )
