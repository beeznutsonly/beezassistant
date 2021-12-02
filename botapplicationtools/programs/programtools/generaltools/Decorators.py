"""
Module containing utility decorators which may
be used by programs
"""

import functools
import time

from prawcore.exceptions import RequestException, ServerError


def consumestransientapierrors(executeFunction):
    """
    Decorator responsible for consuming common transient
    errors which may occur while connecting to the
    Reddit API during the running of the provided
    program
    """

    @functools.wraps(executeFunction)
    def wrapper(*args, **kwargs):
        while True:
            try:
                executeFunction(*args, **kwargs)
                break
            # Handle for problems connecting to the Reddit API
            except (RequestException, ServerError):
                time.sleep(30)
    return wrapper
