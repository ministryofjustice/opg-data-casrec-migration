import functools
import logging
import os
from pathlib import Path

import sys
import time
import psutil

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")
files_used = set([])


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

            log.info(
                f"Function '{function_name}' from '{filename}' ran in "
                f"{time_to_run} secs ",
                extra={
                    "metric": "time_to_run",
                    "value": f"{time_to_run}",
                    "function_name": function_name,
                    "file_name": filename,
                },
            )

    return wrapper


def report_process_mem(position) -> int:
    process = psutil.Process(os.getpid())
    mb = process.memory_info().rss / 1024 / 1024

    return mb


def mem_tracker(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_mem = report_process_mem(position="Start")

        function_path = Path(sys.modules[func.__module__].__file__).parts
        function_name = func.__name__
        filename = function_path[-1]

        try:
            return func(*args, **kwargs)
        finally:
            final_mem = report_process_mem(position="Final")
            log.info(
                f"Done, memory usage: {final_mem-start_mem: .2f} MB.",
                extra={
                    "metric": "memory",
                    "value": f"{final_mem-start_mem: .2f}",
                    "function_name": function_name,
                    "file_name": filename,
                },
            )

    return wrapper


def track_file_use(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        global files_used

        files_used.add(kwargs["file_name"])

        return func(*args, **kwargs)

    return wrapper
