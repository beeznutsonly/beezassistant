class DatabaseConnectionFailureError(Exception):
    """
    Class to encapsulate an error raised when the
    bot's there is an error creating a new database
    connection
    """

    def __init__(self, *args):
        super().__init__(self, args)
