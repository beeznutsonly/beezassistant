import praw
from praw.exceptions import ReadOnlyException
from prawcore import ResponseException

from botapplicationtools.botcredentials.BotCredentials import BotCredentials
from botapplicationtools.botcredentials.InvalidBotCredentialsError import InvalidBotCredentialsError
from botapplicationtools.programs.programtools.generaltools.RedditInterface import RedditInterface


class RedditInterfaceFactory:
    """Factory for RedditInterface objects"""

    __botCredentials: BotCredentials

    def __init__(
            self,
            botCredentials
    ):
        prawReddit = praw.Reddit(
            user_agent=botCredentials.getUserAgent,
            client_id=botCredentials.getClientId,
            client_secret=botCredentials.getClientSecret,
            username=botCredentials.getUsername,
            password=botCredentials.getPassword
        )
        if not self.__authenticated(prawReddit):
            raise InvalidBotCredentialsError

        self.__botCredentials = botCredentials

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

    def getRedditInterface(self) -> RedditInterface:
        """Retrieve new Reddit Interface"""

        prawReddit = praw.Reddit(
            user_agent=self.__botCredentials.getUserAgent,
            client_id=self.__botCredentials.getClientId,
            client_secret=self.__botCredentials.getClientSecret,
            username=self.__botCredentials.getUsername,
            password=self.__botCredentials.getPassword
        )

        return RedditInterface(prawReddit)
