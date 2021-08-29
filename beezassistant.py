#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main script from which the beezassistant bot is run"""

__author__ = "u/beeznutsonly"

import configparser
import logging
import os
import signal
import sqlite3
import sys
import time
from logging.handlers import TimedRotatingFileHandler
from typing import Dict

import psycopg2

from botapplicationtools.botcredentials.BotCredentials import BotCredentials
from botapplicationtools.botcredentials.BotCredentialsDAO import \
    BotCredentialsDAO
from botapplicationtools.botcredentials.InvalidBotCredentialsError import InvalidBotCredentialsError
from botapplicationtools.databasetools.databaseconnectionfactories \
    .DatabaseConnectionFactory import DatabaseConnectionFactory
from botapplicationtools.databasetools.databaseconnectionfactories \
    .PgsqlDatabaseConnectionFactory import PgsqlDatabaseConnectionFactory
from botapplicationtools.databasetools.databaseconnectionfactories \
    .SqliteDatabaseConnectionFactory import SqliteDatabaseConnectionFactory
from botapplicationtools.databasetools.databaseinitializers \
    import DatabaseInitializer
from botapplicationtools.databasetools.exceptions.DatabaseNotFoundError \
    import DatabaseNotFoundError
from botapplicationtools.exceptions.BotInitializationError import \
    BotInitializationError
from botapplicationtools.programrunners.PostsManagerRunner import \
    PostsManagerRunner
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programrunners.SceneInfoArchiverRunner import \
    SceneInfoArchiverRunner
from botapplicationtools.programrunners.StarInfoReplyerRunner import StarInfoReplyerRunner
from botapplicationtools.programrunners.StarsArchiveWikiPageWriterRunner import \
    StarsArchiveWikiPageWriterRunner
from botapplicationtools.programrunners.exceptions \
    .ProgramRunnerInitializationError import ProgramRunnerInitializationError
from botapplicationtools.programs.programtools.generaltools.RedditInterface \
    import RedditInterface
from botapplicationtools.programsexecutors.AsynchronousProgramsExecutor \
    import AsynchronousProgramsExecutor
from botapplicationtools.programsexecutors.ProgramsExecutor import ProgramsExecutor
from botapplicationtools.programsexecutors.exceptions \
    .ProgramsExecutorInitializationError import ProgramsExecutorInitializationError
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory import RedditInterfaceFactory

__RESOURCES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'resources'
)
__mainLogger: logging.Logger
__defaultConsoleLoggingLevel: int
__programsExecutor: ProgramsExecutor


# Bot initialization commands
# -------------------------------------------------------------------------------


def __initializeLogging(logFileName):
    """Initialize the bot's logging apparatus"""

    global __mainLogger
    global __defaultConsoleLoggingLevel

    # Disabling any 3rd party loggers
    for _ in logging.root.manager.loggerDict:
        logging.getLogger(_).setLevel(logging.CRITICAL)

    # Initializing the root logger
    logging.basicConfig(level=logging.DEBUG)
    rootLogger = logging.getLogger()

    # Initializing the main bot application logger
    __mainLogger = logging.getLogger(__name__)

    # Clearing any existing log handlers for program loggers
    for logger in [rootLogger, __mainLogger]:
        if len(logger.handlers):
            logger.handlers.clear()

    # Setting up log handlers
    logFileHandler = TimedRotatingFileHandler(
        filename=logFileName,
        when='D',
        utc=True
    )
    consoleHandler = logging.StreamHandler()
    logFileHandler.set_name('log_file')
    consoleHandler.set_name('console')
    logFileHandler.setFormatter(
        logging.Formatter(
            '[%(asctime)s] %(name)-16s : '
            '%(levelname)-8s - %(message)s'
        )
    )
    consoleHandler.setFormatter(
        logging.Formatter(
            '%(name)-16s : %(message)s'
        )
    )
    logFileHandler.setLevel(logging.DEBUG)
    consoleHandler.setLevel(logging.DEBUG)

    # Adding the handlers to the root logger
    rootLogger.addHandler(logFileHandler)
    rootLogger.addHandler(consoleHandler)

    # Setting the default console logging level global variable
    __defaultConsoleLoggingLevel = consoleHandler.level


def __getInitialConfigReader(configFileName) -> configparser.ConfigParser:
    """Retrieve the bot's config. file reader"""

    configParser = configparser.ConfigParser()
    try:
        with open(configFileName) as configFile:
            configParser.read_file(configFile)

    # Handle when there is a problem reading the config file
    except OSError as ex:
        raise BotInitializationError(
            "An error just occurred while trying to open the "
            "bot's configuration file.", ex
        )

    return configParser


def ___initializeDatabase(connection):
    """Convenience method to initialize the bot's database"""

    sqliteScriptPath = os.path.join(
        __RESOURCES_PATH, 'beezassistant.sql'
    )
    DatabaseInitializer.initializeDatabase(
        connection, sqliteScriptPath
    )


def ___getInitialPgsqlDatabaseConnectionFactory(
        user, password, databaseName
) -> PgsqlDatabaseConnectionFactory:
    """Retrieve an initial postgresql database connection factory"""

    try:

        databaseConnectionFactory = PgsqlDatabaseConnectionFactory(
            user, password, databaseName
        )

    # Handle when database is not found
    except DatabaseNotFoundError:

        __mainLogger.warning(
            "Database not found. The bot is now "
            "creating a new database."
        )

        # Creating new database
        with psycopg2.connect(
                user=user, password=password
        ) as databaseCreationConnection:

            databaseCreationConnection.autocommit = True
            cursor = databaseCreationConnection.cursor()
            cursor.execute('create database {};'.format(
                databaseName
            ))
            cursor.close()

        # Initializing the new database
        with psycopg2.connect(
                user=user,
                password=password,
                dbName=databaseName
        ) as databaseInitializationConnection:
            ___initializeDatabase(databaseInitializationConnection)

        __mainLogger.info("Database successfully created")

        databaseConnectionFactory = PgsqlDatabaseConnectionFactory(
            user, password, databaseName
        )

    return databaseConnectionFactory


def ___getInitialSqliteDatabaseConnectionFactory(databaseFileName)\
        -> SqliteDatabaseConnectionFactory:
    """Retrieve an initial sqlite database connection factory"""

    try:

        databaseConnectionFactory = SqliteDatabaseConnectionFactory(
            databaseFileName
        )

    # Handle when database is not found
    except DatabaseNotFoundError:

        __mainLogger.warning(
            "Database not found. The bot is now "
            "creating a new database."
        )

        # Creating and initializing new database
        with sqlite3.connect(databaseFileName) as connection:
            ___initializeDatabase(connection)

        __mainLogger.info("Database successfully created")
        databaseConnectionFactory = SqliteDatabaseConnectionFactory(
            databaseFileName
        )

    return databaseConnectionFactory


def __getInitialDatabaseConnectionFactory(database, configReader)\
        -> DatabaseConnectionFactory:
    """Retrieve an initial database connection factory"""

    try:
        # For SQLite database
        if database == 'sqlite':
            section = 'SqliteDatabase'
            databaseFilePath = configReader.get(
                section, 'databaseFilePath'
            )
            return ___getInitialSqliteDatabaseConnectionFactory(
                databaseFilePath
            )

        # For PostgresSQL database
        elif database == 'pgsql':
            section = 'PgsqlDatabase'
            user = configReader.get(
                section, 'user'
            )
            password = configReader.get(
                section, 'password'
            )
            databaseName = configReader.get(
                section, 'databaseName'
            )
            return ___getInitialPgsqlDatabaseConnectionFactory(
                user, password, databaseName
            )

        # Handle if database provided is not catered for
        else:
            raise BotInitializationError(
                "The specified database, '{}', is not supported by the bot".format(
                    database
                )
            )

    # Propagate up a Bot Initialization Error
    except BotInitializationError as ex:
        raise ex

    # Handle when an unexpected exception occurs
    except Exception as ex:
        raise BotInitializationError(
            "An error occurred while initializing the bot's "
            "database connection factory ",
            ex
        )


def __getInitialBotCredentials(databaseConnection)\
        -> BotCredentials:
    """Retrieve initial bot credentials"""

    # Checking for bot credentials in environment variables first
    envUserAgent = os.getenv("USER_AGENT")
    envClientId = os.getenv("CLIENT_ID")
    envClientSecret = os.getenv("CLIENT_SECRET")
    envUsername = os.getenv("USERNAME")
    envPassword = os.getenv("PASSWORD")

    if (
            envUserAgent and
            envClientId and
            envClientSecret and
            envUsername and
            envPassword
    ):
        botCredentials = BotCredentials(
            envUserAgent,
            envClientId,
            envClientSecret,
            envUsername,
            envPassword
        )

    # If bot credentials not found
    # in environment variables
    else:

        try:
            # Loading bot credentials from the database
            botCredentialsDAO = BotCredentialsDAO(databaseConnection)
            botCredentials = botCredentialsDAO.getBotCredentials()

        # Handle if there is a problem loading
        # bot credentials from database
        except Exception as ex:
            raise BotInitializationError(
                "Could not load initial bot credentials from "
                "the database.", ex
            )

    return botCredentials


def ___getNewBotCredentials() -> BotCredentials:
    """Convenience method to retrieve bot credentials from user input"""

    try:
        # Prompt for new valid credentials
        while True:

            # Pause console logging while listening for input
            __pauseConsoleLogging()

            user_agent = input("Enter User Agent: ")
            client_id = input("Enter Client ID: ")
            client_secret = input("Enter Client Secret: ")
            username = input("Enter Username: ")
            password = input("Enter Password: ")

            # Resume console logging
            __resumeConsoleLogging()

            return BotCredentials(
                user_agent, client_id,
                client_secret, username,
                password
            )

    # Handle if listening interrupted
    except KeyboardInterrupt or EOFError as ex:
        __resumeConsoleLogging()
        raise ex


def __getInitialRedditInterfaceFactory(botCredentials, databaseConnection) \
        -> RedditInterfaceFactory:
    """ Initialize Reddit Interface Factory"""

    # Attempting to retrieve a valid RedditInterfaceFactory
    # instance from provided credentials

    try:
        redditInterfaceFactory = RedditInterface(botCredentials)

        # Saving the valid bot credentials to storage
        try:
            botCredentialsDAO = BotCredentialsDAO(
                databaseConnection
            )
            botCredentialsDAO.saveBotCredentials(botCredentials)

        # Handle if save operation fails
        except Exception as ex:
            __mainLogger.error(
                "Failed to save bot credentials"
                " to database. Error: {}".format(
                    str(ex.args)
                )
            )
    # Handle if credential authentication fails
    except InvalidBotCredentialsError:
        __mainLogger.error(
            "The provided credentials are invalid. "
            "Please enter new valid credentials"
        )
        try:
            redditInterfaceFactory = __getInitialRedditInterfaceFactory(
                ___getNewBotCredentials(), databaseConnection
            )
        except KeyboardInterrupt or EOFError:
            raise BotInitializationError(
                "Retrieval of bot credentials from user input "
                "aborted"
            )

    return redditInterfaceFactory


def __loadInitialProgramRunners(
        databaseConnectionFactory,
        redditInterfaceFactory,
        configReader
) -> Dict[str, ProgramRunner]:
    """Load initial Program Runners"""

    programRunners = {}

    try:
        programRunners['starsarchivewikipagewriter'] = \
            StarsArchiveWikiPageWriterRunner(
                databaseConnectionFactory=databaseConnectionFactory,
                redditInterfaceFactory=redditInterfaceFactory,
                configReader=configReader
            )
        programRunners['sceneinfoarchiver'] = SceneInfoArchiverRunner(
            databaseConnectionFactory=databaseConnectionFactory,
            redditInterfaceFactory=redditInterfaceFactory,
            configReader=configReader
        )
        programRunners['postsmanager'] = PostsManagerRunner(
            databaseConnectionFactory=databaseConnectionFactory,
            redditInterfaceFactory=redditInterfaceFactory,
            configReader=configReader
        )
        programRunners['starinforeplyer'] = StarInfoReplyerRunner(
            databaseConnectionFactory=databaseConnectionFactory,
            redditInterfaceFactory=redditInterfaceFactory,
            configReader=configReader
        )

    # Handle if there is an error initializing any of the Program Runners
    except ProgramRunnerInitializationError as ex:
        raise BotInitializationError(
            "An error occurred while initializing "
            "the Program Runners.", ex
        )

    return programRunners


def __initializeProgramsExecutor(programRunners, configReader)\
        -> ProgramsExecutor:
    """Initialize the Programs Executor"""

    # Initializing the Programs Executor
    try:
        programsExecutor = AsynchronousProgramsExecutor(
            programRunners,
            configReader
        )

    # Handle if there is an error initializing the Programs Executor
    except ProgramsExecutorInitializationError as ex:
        raise BotInitializationError(
            "An error occurred while initializing "
            "the Programs Executor.", ex
        )

    return programsExecutor


def __initializeBot():
    """Initialize the bot"""

    global __programsExecutor

    # Setting up logging apparatus
    __initializeLogging(os.path.join(
        __RESOURCES_PATH, 'logs', 'beezassistant.log'
    ))

    __mainLogger.info("Initializing the bot")

    try:

        # I/O initialization
        # -------------------------------------------------------------------------------

        # Initializing the config. file reader

        __mainLogger.debug("Initializing the bot's config. file reader")
        configFileName = os.path.join(__RESOURCES_PATH, 'beezassistant.ini')
        configReader = __getInitialConfigReader(configFileName)

        # Initializing bot's database connection factory

        __mainLogger.debug(
            "Initializing the bot's database"
            " connection factory"
        )
        section = 'BotApplication'
        database = configReader.get(
            section, 'database'
        )
        databaseConnectionFactory = \
            __getInitialDatabaseConnectionFactory(database, configReader)

        # Bot attribute initialization
        # -------------------------------------------------------------------------------

        # Initializing the programs executor

        # Retrieving initial bot credentials
        __mainLogger.debug("Retrieving initial bot credentials")
        with databaseConnectionFactory.getConnection() as databaseConnection:
            botCredentials = __getInitialBotCredentials(databaseConnection)

        # Initializing the Reddit Interface Factory
        __mainLogger.debug("Initializing the Reddit Interface Factory")
        with databaseConnectionFactory.getConnection() as databaseConnection:
            redditInterfaceFactory = __getInitialRedditInterfaceFactory(
                botCredentials, databaseConnection
            )

        # Initializing the Program Runners
        programRunners = __loadInitialProgramRunners(
            databaseConnectionFactory, redditInterfaceFactory, configReader
        )

        # Initializing the Programs Executor
        __programsExecutor = __initializeProgramsExecutor(
            programRunners, configReader
        )

        # -------------------------------------------------------------------------------

    # Handle if an initialization error occurs
    except BotInitializationError as er:
        __mainLogger.critical(
            "A fatal error occurred during the "
            "bot's initialization. The application "
            "will now exit. Error(s): " + str(er),
            exc_info=True
        )
        sys.exit(2)  # TODO: May need future cleaning up

    __mainLogger.info("Bot successfully initialized")

# -------------------------------------------------------------------------------


# Bot application commands
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

def __pauseConsoleLogging():
    """Pause console logging across entire application"""

    for handler in logging.getLogger().handlers:
        if handler.name == "console":
            handler.setLevel(logging.CRITICAL)
            return
    __mainLogger.warning(
        "Failed to pause logging because "
        "the console logger was not found"
    )


def __resumeConsoleLogging():
    """Resume console logging across entire application"""

    for handler in logging.getLogger().handlers:
        if handler.name == "console":
            handler.setLevel(__defaultConsoleLoggingLevel)
            return
    __mainLogger.warning(
        "Failed to resume logging because "
        "the console logger was not found"
    )


def __startCommandListener():
    """Start the bot command listener"""

    try:
        while not isBotShutDown():
            # Pause console logging while bot is
            # listening for commands
            __pauseConsoleLogging()

            command = input('Enter bot command: ')

            # Resume console logging once command
            # entered
            __resumeConsoleLogging()

            __processBotCommand(command)

    except BaseException as ex:
        __resumeConsoleLogging()
        raise ex


def __processBotCommand(command):
    """Process a bot command"""

    # For blank command
    if command == '' or command == '\n':
        return

    # For program command
    elif command.startswith('run '):
        __programsExecutor.executeProgram(command.split('run ', 1)[1])

    # For programs status request
    elif command == 'status':

        print('\nPrograms status:')

        # Printing all program statuses
        for program, status in __programsExecutor \
                .getProgramStatuses() \
                .items():
            print('{}\t\t: {}'.format(
                program, status
            ))
        print()

    # For shutdown command
    elif (
            command == 'shutdown' or
            command == 'quit' or
            command == 'exit'
    ):
        shutDownBot()

    else:
        __mainLogger.debug(
            "'{}' is not a valid bot command".format(command)
        )


def __killBot():
    """Forcefully shut down the bot"""

    # Windows kill command
    if (
            sys.platform.startswith('win32') or
            sys.platform.startswith('cygwin')
    ):
        os.kill(os.getpid(), signal.CTRL_BREAK_EVENT)

    # Linux kill command
    os.kill(os.getpid(), signal.SIGKILL)


def shutDownBot(wait=True, shutdownExitCode=0):
    """Shut down the bot"""

    if wait:
        __mainLogger.info(
            'Shutting down the bot. Please wait a bit wait while the '
            'remaining tasks ({}) are being finished off'.format(
                ", ".join(
                    {
                        program: status
                        for (program, status) in __programsExecutor
                        .getProgramStatuses()
                        .items()
                        if status != "DONE"
                    }.keys()
                )
            )
        )
        try:
            __programsExecutor.shutDown(True)
            __mainLogger.info('Bot successfully shut down')
            if shutdownExitCode != 0:
                sys.exit(shutdownExitCode)

        # Handle keyboard interrupt midway through graceful shutdown
        except KeyboardInterrupt:

            __programsExecutor.shutDown(False)
            __mainLogger.warning(
                'Graceful shutdown aborted.'
            )
            __mainLogger.info('Bot shut down')

            # Killing the process (only way to effectively stop all threads)
            __killBot()

    else:
        __programsExecutor.shutDown(False)
        __mainLogger.info('Bot shut down')

        __killBot()


def isBotShutDown():
    """Check if bot is shutdown"""

    return __programsExecutor and __programsExecutor.isShutDown()


def startBot(args=[]):
    """Start up the bot"""

    # Initializing the bot
    __initializeBot()

    try:
        # Retrieve additional bot instructions if present
        if len(args) > 0:

            botCommand = ''

            # Retrieve and execute bot command if present
            if len(args) > 1:
                botCommand = " ".join(args[2:])

            __processBotCommand(botCommand)
            __mainLogger.info('The bot is now running')

            try:

                listen = int(args[0])  # Command listening setting

                # Check if command listening is set
                if listen:
                    __startCommandListener()

            # Handle if provided listen argument is invalid
            except ValueError:
                __mainLogger.error(
                    "The provided 'listen' argument, \"{}\", is invalid. "
                    "The bot will therefore shutdown once all of its tasks"
                    " are completed.".format(args[0])
                )

        else:
            # Default to listening for commands if
            # no additional instructions specified
            __mainLogger.info('The bot is now running')
            __startCommandListener()

    # Handle forced shutdown request
    except KeyboardInterrupt or EOFError:
        __mainLogger.warning(
            'Forced bot shutdown requested. Please wait a bit wait while '
            'a graceful shutdown is attempted or press '
            'Ctrl+C to exit immediately'
        )
        shutDownBot(True, 1)

    # Handle unknown exception while bot is running
    except BaseException:
        __mainLogger.critical(
            "A fatal error just occurred while the bot was "
            "running. Please wait a bit wait while "
            "a graceful shutdown is attempted or press "
            "Ctrl+C to exit immediately", exc_info=True
        )
        shutDownBot(True, 2)

# -------------------------------------------------------------------------------


# Let the games begin boysss
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
if __name__ == "__main__":

    # Setting up interrupt signal handler
    signal.signal(signal.SIGINT, signal.default_int_handler)

    # Start bot
    if len(sys.argv) == 1:
        startBot()
    else:
        startBot(sys.argv)

    try:
        # Wait for tasks to complete before shutdown
        while True:
            if not ("RUNNING" in __programsExecutor.getProgramStatuses().values()):
                break
            time.sleep(1)
    finally:
        # Shut bot down if not already
        if not isBotShutDown():
            shutDownBot()
