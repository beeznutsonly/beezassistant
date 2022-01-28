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
            try:
                programLogger = getattr(args[0], '_programLogger', None)
            except IndexError:
                programLogger = None
            while True:
                try:
                    functionValue = executeFunction(*args, **kwargs)
                    return functionValue
                # Handle for problems connecting to the Reddit API
                except (RequestException, ServerError) as ex:
                    message = "Failed to connect to the Reddit API: {}".format(
                                ex.args
                    )
                    if programLogger:
                        programLogger.warning(
                            message
                        )
                    else:
                        print(message)
                    time.sleep(timeout)
        return wrapper

    # Handle if decorator is called with arguments
    if _executeFunction is None:
        return subsuming_function
    else:
        return subsuming_function(_executeFunction)
