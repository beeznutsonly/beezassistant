import praw
from praw.exceptions import ReadOnlyException
from prawcore import ResponseException

from botapplicationtools.botcredentials.BotCredentials import BotCredentials
from botapplicationtools.botcredentials.BotCredentialsDAO import BotCredentialsDAO
from botapplicationtools.botcredentials.InvalidBotCredentialsError import InvalidBotCredentialsError
from botapplicationtools.programs.programtools.generaltools.RedditInterface import RedditInterface


class RedditInterfaceFactory:
    """Factory for RedditInterface objects"""

    __defaultBotCredentials: BotCredentials
    __botCredentialsDAO: BotCredentialsDAO

    def __init__(
            self,
            defaultBotCredentials: BotCredentials,
            botCredentialsDAO: BotCredentialsDAO
    ):
        prawReddit = praw.Reddit(
            user_agent=defaultBotCredentials.getUserAgent,
            client_id=defaultBotCredentials.getClientId,
            client_secret=defaultBotCredentials.getClientSecret,
            username=defaultBotCredentials.getUsername,
            password=defaultBotCredentials.getPassword
        )
        if not self.__authenticated(prawReddit):
            raise InvalidBotCredentialsError

        self.__defaultBotCredentials = defaultBotCredentials
        self.__botCredentialsDAO = botCredentialsDAO

    @staticmethod
    def __authenticated(prawRedditInstance) -> bool:
        """
        Convenience method to authenticate bot credentials
        provided to Reddit instance
        """

        try:
            return not (prawRedditInstance.user.me() is None)
        except ResponseException or ReadOnlyException:
            return False

    def getRedditInterface(self, userProfile: str = None) -> RedditInterface:
        """Retrieve new Reddit Interface"""

        if not bool(userProfile):
            botCredentials = self.__defaultBotCredentials
        else:
            botCredentials = self.__botCredentialsDAO.getBotCredentials(
                userProfile
            )
        prawReddit = praw.Reddit(
            user_agent=botCredentials.getUserAgent,
            client_id=botCredentials.getClientId,
            client_secret=botCredentials.getClientSecret,
            username=botCredentials.getUsername,
            password=botCredentials.getPassword
        )
        return RedditInterface(prawReddit)
