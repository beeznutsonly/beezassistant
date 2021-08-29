# -*- coding: utf-8 -*

class InitializationError(Exception):
    """
    Class to encapsulate an error in the
    initialization of a module
    """

    def __init__(self, *args):
        super().__init__(self, args)
