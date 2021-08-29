# -*- coding: utf-8 -*

from botapplicationtools.exceptions.InitializationError import InitializationError


class ProgramRunnerInitializationError(InitializationError):
    """
    Class to encapsulate an error in the initialization
    of a program runner module
    """

    def __init__(self, *args):
        super().__init__(*args)
