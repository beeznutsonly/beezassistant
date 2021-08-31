class SubmissionReplyDetails:

    __url: str
    __reply: str
    __oneOff: bool

    def __init__(
            self,
            url,
            reply,
            oneOff
    ):
        self.__url = url
        self.__reply = reply
        self.__oneOff = oneOff

    @property
    def getUrl(self):
        return self.__url

    @property
    def getReply(self):
        return self.__reply

    @property
    def getOneOff(self):
        return self.__oneOff
