import functools
import logging
import os
from pathlib import Path

import sys
import time


log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        t = time.process_time()

        function_path = Path(sys.modules[func.__module__].__file__).parts
        function_name = func.__name__
        filename = function_path[-1]

        try:
            return func(*args, **kwargs)

        finally:
            time_to_run = round(time.process_time() - t, 2)

            log.debug(
                f"Function '{function_name}' from '{filename}' ran in "
                f"{time_to_run} secs "
            )

    return wrapper
