"""
Module containing utility decorators which may
be used by programs
"""

import functools
import time

from prawcore.exceptions import RequestException, ServerError


def consumestransientapierrors(_executeFunction=None, *, timeout: int = 30):
    """
    Decorator responsible for consuming common transient
    errors which may occur while connecting to the
    Reddit API during the running of the provided
    program
    """

    def subsuming_function(executeFunction):

        @functools.wraps(executeFunction)
        def wrapper(*args, **kwargs):
            while True:
                try:
                    executeFunction(*args, **kwargs)
                    break
                # Handle for problems connecting to the Reddit API
                except (RequestException, ServerError):
                    time.sleep(timeout)
        return wrapper

    # Handle if decorator is called with arguments
    if _executeFunction is None:
        return subsuming_function
    else:
        return subsuming_function(_executeFunction)
