# -*- coding: utf-8 -*

"""
Class to encapsulate an error in the initialization of a program runner module
"""

from botapplicationtools.exceptions.InitializationError import InitializationError


class ProgramRunnerInitializationError(InitializationError):

    def __init__(self, *args):
        super().__init__(*args)
