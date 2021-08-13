#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "u/beeznutsonly"

"""
Main script from which the beezassistant bot is run
"""

import configparser
import json
import logging
import os
import signal
import sys
import time
from logging.handlers import TimedRotatingFileHandler

import praw
from praw.exceptions import ReadOnlyException
from prawcore import ResponseException

from botapplicationtools.botcredentials.BotCredentials import BotCredentials
from botapplicationtools.botcredentials.BotCredentialsDAO import \
    BotCredentialsDAO
from botapplicationtools.databasetools import SqliteDatabaseInitializer
from botapplicationtools.databasetools.databaseconnectionfactories.SqliteDatabaseConnectionFactory import \
    SqliteDatabaseConnectionFactory
from botapplicationtools.exceptions.BotInitializationError import \
    BotInitializationError
from botapplicationtools.exceptions.InitializationError import \
    InitializationError
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programrunners.ProgramRunnerIO import ProgramRunnerIO
from botapplicationtools.programs.programtools.generaltools.RedditInterface import \
    RedditInterface
from botapplicationtools.programsexecutors.AsynchronousProgramsExecutor import \
    AsynchronousProgramsExecutor

__RESOURCES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'resources'
)
__mainLogger: logging.Logger
__defaultConsoleLoggingLevel: int
__programsExecutor: AsynchronousProgramsExecutor


# Bot initialization commands
# -------------------------------------------------------------------------------

# Initialize the bot's logging apparatus
def __initializeLogging(logFileName):

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


# Retrieve an initial sqlite database connection factory
def __getInitialSqliteDatabaseConnectionFactory(databaseFileName):

    try:

        databaseConnectionFactory = SqliteDatabaseConnectionFactory(
            databaseFileName
        )

    # Handle when database is not found
    except FileNotFoundError:

        __mainLogger.warning(
            "Database not found. The bot is now "
            "creating a new database."
        )

        # Creating new database

        SqliteScriptPath = os.path.join(
            __RESOURCES_PATH, 'beezassistant.sql'
        )

        try:
            SqliteDatabaseInitializer.initializeDatabase(
                databaseFileName, SqliteScriptPath
            )
            __mainLogger.info("Database successfully created")
            databaseConnectionFactory = SqliteDatabaseConnectionFactory(
                databaseFileName
            )

        # Handle if database creation fails
        except Exception as ex:
            raise BotInitializationError(
                "An error occurred while trying to create the "
                "bot's database.",
                ex
            )

    return databaseConnectionFactory


# Retrieve initial bot credentials
def __getInitialBotCredentials(databaseConnection):

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

    # If bot credentials not found in environment variables
    else:

        try:
            # Loading bot credentials from the database
            botCredentialsDAO = BotCredentialsDAO(databaseConnection)
            botCredentials = botCredentialsDAO.getBotCredentials()

        except Exception as ex:
            raise BotInitializationError(
                "Could not load initial bot credentials from "
                "the database.", ex
            )

    return botCredentials


# Retrieve the bot's config. file reader
def __getInitialConfigReader(configFileName):

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


# Convenience method to retrieve bot credentials from user input
def ___getNewBotCredentials():
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


# Convenience method to authenticate bot credentials
def ___authenticated(redditInstance):
    try:
        if redditInstance.user.me() is None:
            return False
    except ResponseException or ReadOnlyException:
        return False
    return True


# Initialize Reddit Interface
def __getInitialRedditInterface(botCredentials, databaseConnection):

    # Attempting to retrieve a valid Praw instance from
    # provided credentials

    prawReddit = praw.Reddit(
        user_agent=botCredentials.getUserAgent(),
        client_id=botCredentials.getClientId(),
        client_secret=botCredentials.getClientSecret(),
        username=botCredentials.getUsername(),
        password=botCredentials.getPassword()
    )

    __mainLogger.debug("Authenticating credentials ...")

    if ___authenticated(prawReddit):

        __mainLogger.debug("Credentials authenticated.")
        redditInterface = RedditInterface(prawReddit)

    # Handle if credential authentication fails
    else:
        __mainLogger.error(
            "The provided credentials are invalid. "
            "Please enter new valid credentials"
        )
        try:
            redditInterface = __getInitialRedditInterface(
                ___getNewBotCredentials(), databaseConnection
            )
        except KeyboardInterrupt or EOFError:
            raise BotInitializationError(
                "Retrieval of bot credentials from user input "
                "aborted"
            )

    # Saving the bot credentials to storage
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

    return redditInterface


# Initialize Program Runner
def __initializeProgramRunner(programRunnerIO, redditInterface):

    # Initializing the Program Runner
    try:
        programRunner = ProgramRunner(
            programRunnerIO,
            redditInterface
        )

    # Handle if there is an error initializing the Program Runner
    except Exception as ex:
        raise BotInitializationError(
            "An error occurred while initializing "
            "the Program Runner.", ex
        )

    return programRunner


# Initialize the bot
def __initializeBot():

    global __programsExecutor

    # Setting up logging apparatus
    __initializeLogging(os.path.join(
        __RESOURCES_PATH, 'logs', 'beezassistant.log'
    ))

    __mainLogger.info("Initializing the bot")

    try:

        # I/O initialization
        # -------------------------------------------------------------------------------

        # Initializing bot's database connection factory

        __mainLogger.debug(
            "Initializing the bot's database"
            " connection factory"
        )
        databaseString = os.path.join(__RESOURCES_PATH, 'beezassistant.db')
        databaseConnectionFactory = \
            __getInitialSqliteDatabaseConnectionFactory(databaseString)

        # Initializing the config. file reader

        __mainLogger.debug("Initializing the bot's config. file reader")
        configFileName = os.path.join(__RESOURCES_PATH, 'beezassistant.ini')
        configReader = __getInitialConfigReader(configFileName)

        # Bot attribute initialization
        # -------------------------------------------------------------------------------

        # Initializing the programs executor

        # Retrieving initial bot credentials
        __mainLogger.debug("Retrieving initial bot credentials")
        with databaseConnectionFactory.getConnection() as databaseConnection:
            botCredentials = __getInitialBotCredentials(databaseConnection)

        # Initializing the Reddit Interface
        __mainLogger.debug("Initializing the Reddit Interface")
        with databaseConnectionFactory.getConnection() as databaseConnection:
            redditInterface = __getInitialRedditInterface(
                botCredentials, databaseConnection
            )

        # Initializing the Program Runner
        __mainLogger.debug("Initializing the Program Runner")
        programRunnerIO = ProgramRunnerIO(
            configReader, databaseConnectionFactory
        )
        programRunner = __initializeProgramRunner(
            programRunnerIO, redditInterface
        )

        # Initializing the Programs Executor
        __mainLogger.debug("Initializing the bot's Programs Executor")
        __programsExecutor = AsynchronousProgramsExecutor(
            programRunner, configReader
        )

        # -------------------------------------------------------------------------------

    # Handle if an initialization error occurs
    except InitializationError as er:
        __mainLogger.critical(
            "A fatal error occurred during the "
            "bot's initialization. The application "
            "will now exit. Error(s): " + str(er),
            exc_info=True
        )
        sys.exit(2) # May need future cleaning up

    __mainLogger.info("Bot successfully initialized")

# -------------------------------------------------------------------------------


# Bot application commands
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

# Pause console logging across entire application
def __pauseConsoleLogging():

    for handler in logging.getLogger().handlers:
        if handler.name == "console":
            handler.setLevel(logging.CRITICAL)
            return
    __mainLogger.warning(
        "Failed to pause logging because "
        "the console logger was not found"
    )


# Resume console logging across entire application
def __resumeConsoleLogging():
    for handler in logging.getLogger().handlers:
        if handler.name == "console":
            handler.setLevel(__defaultConsoleLoggingLevel)
            return
    __mainLogger.warning(
        "Failed to resume logging because "
        "the console logger was not found"
    )


# Start up the bot
def startBot(args=sys.argv):

    # Initializing the bot
    __initializeBot()

    try:
        # Retrieve additional bot instructions if present
        if len(args) > 1:

            botCommand = ''

            # Retrieve and execute bot command if present
            if len(args) > 2:
                botCommand = " ".join(args[2:])

            __processBotCommand(botCommand)
            __mainLogger.info('The bot is now running')

            try:

                listen = int(args[1])  # Command listening setting

                # Check if command listening is set
                if listen:
                    __startCommandListener()

            # Handle if provided listen argument is invalid
            except ValueError:
                __mainLogger.error(
                    "The provided 'listen' argument, \"{}\", is invalid. "
                    "The bot will therefore shutdown once all of its tasks"
                    " are completed.".format(args[1])
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


# Start the bot command listener
def __startCommandListener():
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


# Process a bot command
def __processBotCommand(command):

    # Blank command
    if command == '' or command == '\n':
        return
    # For program command
    elif command.startswith('run '):
        __programsExecutor.executeProgram(command.split('run ', 1)[1])

    # For programs status request
    elif command == 'status':

        print('\nPrograms status:')
        
        # Printing all program statuses
        for program, status in \
            __programsExecutor \
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


# Shut down the bot
def shutDownBot(wait=True, shutdownExitCode=0):

    if wait:
        __mainLogger.info(
            'Shutting down the bot. Please wait a bit wait while the '
            'remaining tasks ({}) are being finished off'.format(
                ", ".join(
                    {
                        program: status
                        for (program, status) in
                        __programsExecutor
                        .getProgramStatuses()
                        .items()
                        if status != "DONE"
                    }.keys()
                )
            )
        )
        try:
            __programsExecutor.shutdown(True)
            __mainLogger.info('Bot successfully shut down')
            if shutdownExitCode != 0:
                sys.exit(shutdownExitCode)

        # Handle keyboard interrupt midway through graceful shutdown
        except KeyboardInterrupt:

            __programsExecutor.shutdown(False)
            __mainLogger.warning(
                'Graceful shutdown aborted.'
            )
            __mainLogger.info('Bot shut down')
            
            # Process killers (only way to effectively stop all threads)

            # Windows kill command
            if (
                    sys.platform.startswith('win32') or
                    sys.platform.startswith('cygwin')
            ):
                os.kill(os.getpid(), signal.CTRL_BREAK_EVENT)

            # Linux kill command
            os.kill(os.getpid(), signal.SIGKILL)

    else:
        __programsExecutor.shutdown(False)
        __mainLogger.info('Bot shut down')
        
        # Windows kill command
        if (
                sys.platform.startswith('win32') or
                sys.platform.startswith('cygwin')
        ):
            os.kill(os.getpid(), signal.CTRL_BREAK_EVENT)

        # Linux kill command
        os.kill(os.getpid(), signal.SIGKILL)

    
# Check if bot is shutdown
def isBotShutDown():
    return __programsExecutor and __programsExecutor.isShutDown()


# -------------------------------------------------------------------------------


# Let the games begin boysss
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
if __name__ == "__main__":

    # Setting up shutdown signal handler
    signal.signal(signal.SIGINT, signal.default_int_handler)

    # Start
    startBot()
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

