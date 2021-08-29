# -*- coding: utf-8 -*

class DatabaseNotFoundError(Exception):
    """
    Class to encapsulate an error raised when the
    bot's database does not exist
    """

    def __init__(self, *args):
        super().__init__(self, args)
