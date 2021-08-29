# -*- coding: utf-8 -*

from botapplicationtools.exceptions.InitializationError import InitializationError


class ProgramsExecutorInitializationError(InitializationError):
    """
    Class to encapsulate an error in the initialization
    of a Programs Executor module
    """

    def __init__(self, *args):
        super().__init__(*args)
