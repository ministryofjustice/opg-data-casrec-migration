import logging
from datetime import datetime
import colorlog as colourlog
from pythonjsonlogger import jsonlogger


class MyHandler(colourlog.StreamHandler):
    def __init__(self, env=None):
        self.env = env

        colourlog.StreamHandler.__init__(self)

        formatter = CustomColouredFormatter(
            datefmt="%Y-%m-%dT%T%Z",
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


class CustomColouredFormatter(colourlog.ColoredFormatter):
    def format(self, record: logging.LogRecord) -> str:
        default_attrs = logging.LogRecord(
            None, None, None, None, None, None, None
        ).__dict__.keys()
        extras = set(record.__dict__.keys()) - default_attrs

        fmt = "%(log_color)s %(asctime)s %(filename)-18s %(levelname)-8s: %(message)s"
        for attr in extras:
            fmt += f'; "{attr}": "%({attr})s"'

        self._style._fmt = fmt

        return super().format(record)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


class ContextFilter(logging.Filter):
    def __init__(self, db_config=None, module_details=None):
        self.db_config = db_config
        self.module_details = module_details

    def filter(self, record):
        record.module_details = self.module_details
        if self.db_config:
            db_conf = {
                "source_schema": self.db_config.get("source_schema", None),
                "target_schema": self.db_config.get("target_schema", None),
                "chunk_size": self.db_config.get("chunk_size", None),
            }
            record.db_config = db_conf

        return True


def setup_logging(env, level=None, db_config=None, module_name=None):
    log = logging.getLogger("root")

    VERBOSE_LEVELV_NUM = 5
    logging.addLevelName(VERBOSE_LEVELV_NUM, "VERBOSE")

    def verbose(self, message, *args, **kws):
        if self.isEnabledFor(VERBOSE_LEVELV_NUM):
            self._log(VERBOSE_LEVELV_NUM, message, args, **kws)

    logging.Logger.verbose = verbose

    DATA_LEVELV_NUM = 5
    logging.addLevelName(DATA_LEVELV_NUM, "VERBOSE")

    def data(self, message, *args, **kws):
        if self.isEnabledFor(DATA_LEVELV_NUM):
            self._log(DATA_LEVELV_NUM, message, args, **kws)

    logging.Logger.data = data

    # envcheck - just setting log levels for local dev
    if env == "local":
        level = level if level else "VERBOSE"
        log.addHandler(MyHandler())
    else:
        level = level if level else "DEBUG"
        logHandler = logging.StreamHandler()
        formatter = CustomJsonFormatter(
            "%(timestamp)s %(level)s %(funcName)s %(message)s"
        )
        logHandler.setFormatter(formatter)
        log.addHandler(logHandler)
        try:
            auto_filter = ContextFilter(db_config, module_name)
            log.addFilter(auto_filter)
        except Exception:
            pass
    log.setLevel(level)
    log.info(f"{level} logging enabled for environment {env}")

    return log
