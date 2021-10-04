from configparser import ConfigParser

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.MessageCommandProcessorRunner import MessageCommandProcessorRunner
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programrunners.SceneInfoArchiverRunner import SceneInfoArchiverRunner
from botapplicationtools.programrunners.ScheduledCrossposterRunner import ScheduledCrossposterRunner
from botapplicationtools.programrunners.ScheduledPosterRunner import ScheduledPosterRunner
from botapplicationtools.programrunners.StarInfoReplyerRunner import StarInfoReplyerRunner
from botapplicationtools.programrunners.StarsArchiveWikiPageWriterRunner import StarsArchiveWikiPageWriterRunner
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory import RedditInterfaceFactory


class ProgramRunnerFactory:

    __redditInterfaceFactory: RedditInterfaceFactory
    __databaseConnectionFactory: DatabaseConnectionFactory
    __configReader: ConfigParser

    def __init__(
            self,
            redditInterfaceFactory: RedditInterfaceFactory,
            databaseConnectionFactory: DatabaseConnectionFactory,
            configReader: ConfigParser
    ):
        self.__redditInterfaceFactory = redditInterfaceFactory
        self.__databaseConnectionFactory = databaseConnectionFactory
        self.__configReader = configReader

    def getProgramRunner(self, programName: str) -> ProgramRunner:

        programNameLower = programName.lower()
        databaseConnectionFactory = self.__databaseConnectionFactory
        redditInterfaceFactory = self.__redditInterfaceFactory
        configReader = self.__configReader

        if programNameLower == 'starsarchivewikipagewriter':
            return StarsArchiveWikiPageWriterRunner(
                databaseConnectionFactory=databaseConnectionFactory,
                redditInterfaceFactory=redditInterfaceFactory,
                configReader=configReader
            )
        elif programNameLower == 'sceneinfoarchiver':
            return SceneInfoArchiverRunner(
                databaseConnectionFactory=databaseConnectionFactory,
                redditInterfaceFactory=redditInterfaceFactory,
                configReader=configReader
            )
        elif programNameLower == 'starinforeplyer':
            return StarInfoReplyerRunner(
                databaseConnectionFactory=databaseConnectionFactory,
                redditInterfaceFactory=redditInterfaceFactory,
                configReader=configReader
            )
        elif programNameLower == 'messagecommandprocessor':
            return MessageCommandProcessorRunner(
                databaseConnectionFactory=databaseConnectionFactory,
                redditInterfaceFactory=redditInterfaceFactory,
                configReader=configReader
            )
        elif programNameLower == 'scheduledcrossposter':
            return ScheduledCrossposterRunner(
                databaseConnectionFactory=databaseConnectionFactory,
                redditInterfaceFactory=redditInterfaceFactory,
                configReader=configReader
            )
        elif programNameLower == 'scheduledposter':
            return ScheduledPosterRunner(
                databaseConnectionFactory=databaseConnectionFactory,
                redditInterfaceFactory=redditInterfaceFactory,
                configReader=configReader
            )
        else:
            return None
