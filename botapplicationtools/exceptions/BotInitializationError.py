# -*- coding: utf-8 -*

"""
Class to encapsulate an error in the initialization of a bot module
"""

from botapplicationtools.exceptions.InitializationError import InitializationError


class BotInitializationError(InitializationError):

    def __init__(self, *args):
        super().__init__(*args)