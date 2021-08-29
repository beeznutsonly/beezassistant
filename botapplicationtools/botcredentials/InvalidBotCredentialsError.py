class InvalidBotCredentialsError(Exception):
    """
    Class encapsulating an exception raised
    when provided bot credentials are invalid
    """

    def __init__(self, *args):
        super().__init__(self, args)
