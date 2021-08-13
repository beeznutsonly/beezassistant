# -*- coding: utf-8 -*-

"""
Class holding the bot's credentials
"""


class BotCredentials:

    __user_agent = None
    __client_id = None
    __client_secret = None
    __username = None
    __password = None

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

    def getUserAgent(self):
        return self.__user_agent

    def getClientId(self):
        return self.__client_id

    def getClientSecret(self):
        return self.__client_secret

    def getUsername(self):
        return self.__username

    def getPassword(self):
        return self.__password

    # This is here for obvious reasons
    def clearCredentials(self):
        self.__user_agent = None
        self.__client_id = None
        self.__client_secret = None
        self.__username = None
        self.__password = None
