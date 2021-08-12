# -*- coding: utf-8 -*

"""
Class to encapsulate an error in the initialization of a module
"""


class InitializationError(Exception):

    def __init__(self, *args):
        super().__init__(self, args)
