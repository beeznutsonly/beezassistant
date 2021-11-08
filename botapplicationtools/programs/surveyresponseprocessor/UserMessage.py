class UserMessage:

    __subject: str
    __body: str

    def __init__(
            self,
            subject: str,
            body: str
    ):
        self.__subject = subject
        self.__body = body

    @property
    def getSubject(self):
        return self.__subject

    @property
    def getBody(self):
        return self.__body
