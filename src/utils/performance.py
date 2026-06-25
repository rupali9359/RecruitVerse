import time
from functools import wraps

from src.utils.logger import (
    logger
)


def measure_time(
        function):

    @wraps(
        function
    )
    def wrapper(
            *args,
            **kwargs):

        start = time.time()

        result = function(
            *args,
            **kwargs
        )

        end = time.time()

        execution_time = round(
            end - start,
            4
        )

        logger.info(
            f"{function.__name__} executed in {execution_time} seconds"
        )

        return result

    return wrapper


def get_execution_time(
        start_time):

    return round(
        time.time() - start_time,
        4
    )