
class DatabaseNotFoundError(Exception):

    def __init__(self, *args):
        super().__init__(self, args)