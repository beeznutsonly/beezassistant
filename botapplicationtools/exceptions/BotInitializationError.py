# -*- coding: utf-8 -*

from botapplicationtools.exceptions.InitializationError import InitializationError


class BotInitializationError(InitializationError):
    """
    Class to encapsulate an error in the
    initialization of a bot module
    """

    def __init__(self, *args):
        super().__init__(*args)
