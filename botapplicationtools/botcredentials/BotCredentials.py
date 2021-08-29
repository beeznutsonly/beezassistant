# -*- coding: utf-8 -*-

class BotCredentials:
    """
    Class holding the bot's credentials
    """

    __user_agent: str
    __client_id: str
    __client_secret: str
    __username: str
    __password: str

    def __init__(
            self,
            user_agent,
            client_id,
            client_secret,
            username,
            password
    ):
        self.__user_agent = user_agent
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__username = username
        self.__password = password

    @property
    def getUserAgent(self):
        """Retrieve the bot's User Agent"""

        return self.__user_agent

    @property
    def getClientId(self):
        """Retrieve the bot's Client ID"""

        return self.__client_id

    @property
    def getClientSecret(self):
        """Retrieve the bot's Client Secret"""

        return self.__client_secret

    @property
    def getUsername(self):
        """Retrieve the bot's Username"""

        return self.__username

    @property
    def getPassword(self):
        """Retrieve the bot's Password"""

        return self.__password

    # This is here for obvious reasons
    def clearCredentials(self):
        """Convenience method to clear the bot's credentials"""

        self.__user_agent = None
        self.__client_id = None
        self.__client_secret = None
        self.__username = None
        self.__password = None
