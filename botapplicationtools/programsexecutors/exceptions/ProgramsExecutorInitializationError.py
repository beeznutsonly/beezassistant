# -*- coding: utf-8 -*

"""
Class to encapsulate an error in the initialization of a Programs Executor module
"""

from botapplicationtools.exceptions.InitializationError import InitializationError


class ProgramsExecutorInitializationError(InitializationError):

    def __init__(self, *args):
        super().__init__(*args)