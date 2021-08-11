#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "u/beeznutsonly"

from praw.exceptions import ReadOnlyException

"""
Main script from which the beezassistant bot is run
"""

import configparser
import json
import logging
import os.path
import sys
from concurrent.futures import ThreadPoolExecutor
from logging.handlers import TimedRotatingFileHandler

import praw
from prawcore import ResponseException

from botapplicationtools.botcredentials.BotCredentials import BotCredentials
from botapplicationtools.botcredentials.BotCredentialsDAO import BotCredentialsDAO
from botapplicationtools.databasetools import SqliteDatabaseInitializer
from botapplicationtools.databasetools.databaseconnectionfactories \
    .SqliteDatabaseConnectionFactory \
    import SqliteDatabaseConnectionFactory
from botapplicationtools.exceptions.InitializationError \
    import InitializationError
from botapplicationtools.programrunner.ProgramRunner \
    import ProgramRunner
from botapplicationtools.programrunner.ProgramRunnerIO \
    import ProgramRunnerIO
from botapplicationtools.programs.programtools.generaltools.RedditInterface \
    import RedditInterface
from botapplicationtools.programsexecutors.AsynchronousProgramsExecutor \
    import AsynchronousProgramsExecutor

# Bot application initialization
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

# I/O initialization
# -------------------------------------------------------------------------------

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
RESOURCES_PATH = os.path.join(BASE_PATH, 'resources')

# Logging configuration

# Logging I/O
LOGS_PATH = os.path.join(RESOURCES_PATH, 'logs')
LOG_FILE = os.path.join(LOGS_PATH, 'beezassistant.log')

logging.basicConfig(level=logging.DEBUG)  # Initializing the root logger

for _ in logging.root.manager.loggerDict:  # Disable any 3rd party loggers
    logging.getLogger(_).setLevel(logging.CRITICAL)

# Initializing loggers to be used
ROOT_LOGGER = logging.getLogger()
MAIN_LOGGER = logging.getLogger(__name__)
PROGRAM_RUNNER_LOGGER = logging.getLogger('programRunner')
PROGRAMS_EXECUTOR_LOGGER = logging.getLogger('programsExecutor')

# Clearing any existing log handlers
for logger in [
    ROOT_LOGGER, MAIN_LOGGER, PROGRAM_RUNNER_LOGGER,
    PROGRAMS_EXECUTOR_LOGGER
]:
    if len(logger.handlers):
        logger.handlers.clear()

# Setting up log handlers
CONSOLE_HANDLER = logging.StreamHandler()
LOG_FILE_HANDLER = TimedRotatingFileHandler(
    filename=LOG_FILE,
    when='D',
    utc=True
)
LOG_FILE_HANDLER.setFormatter(
    logging.Formatter(
        '[%(asctime)s] %(name)-16s : '
        '%(levelname)-8s - %(message)s'
    )
)
CONSOLE_HANDLER.setFormatter(
    logging.Formatter(
        '%(name)-16s : %(message)s'
    )
)
LOG_FILE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setLevel(logging.DEBUG)

# Adding the handlers to the root logger
ROOT_LOGGER.addHandler(LOG_FILE_HANDLER)
ROOT_LOGGER.addHandler(CONSOLE_HANDLER)

MAIN_LOGGER.debug("Initializing the bot")

# Loading bot information from database
MAIN_LOGGER.debug("Loading bot information from database")

DATABASE_PATH = os.path.join(RESOURCES_PATH, 'beezassistant.db')
DATABASE_CONNECTION_FACTORY = None

try:

    DATABASE_CONNECTION_FACTORY = SqliteDatabaseConnectionFactory(
        DATABASE_PATH
    )

# Handle when database is not found
except FileNotFoundError as ex:

    MAIN_LOGGER.warning(
        "Database not found. The bot is now "
        "creating a new database."
    )

    # Creating new database

    SqliteScriptPath = os.path.join(RESOURCES_PATH, 'beezassistant.sql')

    try:
        SqliteDatabaseInitializer.initializeDatabase(
            DATABASE_PATH, SqliteScriptPath
        )
        DATABASE_CONNECTION_FACTORY = SqliteDatabaseConnectionFactory(
            DATABASE_PATH
        )

    # Handle if database creation fails
    except Exception as ex:
        MAIN_LOGGER.critical(
            "A fatal error just while trying to create the "
            "bot's database. Error(s): " + str(ex.args),
            exc_info=True
        )
        sys.exit(3)

    MAIN_LOGGER.info("Database successfully created")

# Loading bot credentials from the database
databaseConnection = DATABASE_CONNECTION_FACTORY.getConnection()
botCredentialsDAO = BotCredentialsDAO(databaseConnection)
botCredentials = botCredentialsDAO.getBotCredentials()
databaseConnection.close()

# Loading initial bot application settings from config file

MAIN_LOGGER.debug(
    "Loading initial bot application "
    "settings from config file"
)

# Loading the bot's configuration file
CONFIG_FILE = os.path.join(RESOURCES_PATH, 'beezassistant.ini')
CONFIG_PARSER = configparser.ConfigParser()
try:
    CONFIG_PARSER.read_file(open(CONFIG_FILE))

# Handle when there is a problem reading the config file
except OSError as ex:
    MAIN_LOGGER.critical(
        "A fatal error just occurred while trying to open the "
        "bot's configuration file. Error(s): " + str(ex.args),
        exc_info=True
    )
    sys.exit(3)

# Loading values from configuration file
try:

    # Initial program commands
    INITIAL_PROGRAM_COMMANDS = json.loads(CONFIG_PARSER.get(
        'BotApplication', 'initialprogramcommands'
    ))

# Handle when there is a problem parsing the config file
except configparser.Error or json.JSONDecodeError as ex:
    MAIN_LOGGER.critical(
        "A fatal error just occurred while parsing "
        "the configuration file for the bot application's "
        "initial variable values. Error(s): " + str(ex.args),
        exc_info=True
    )
    sys.exit(2)


# Non-I/O initialization
# -------------------------------------------------------------------------------

# Initializing the Reddit Interface

MAIN_LOGGER.debug("Initialializing the Reddit Interface")

# Attempting to retrieve a valid Praw instance from
# provided credentials
PRAW_REDDIT = praw.Reddit(
    user_agent=botCredentials.getUserAgent(),
    client_id=botCredentials.getClientId(),
    client_secret=botCredentials.getClientSecret(),
    username=botCredentials.getUsername(),
    password=botCredentials.getPassword()
)


# Convenience method to authenticate bot credentials
def __authenticated(redditInstance):
    try:
        MAIN_LOGGER.info("Authenticating credentials...")
        if redditInstance.user.me() is None:
            return False
        MAIN_LOGGER.info("Credentials authenticated")
    except ResponseException or ReadOnlyException:
        return False
    return True


if __authenticated(PRAW_REDDIT):
    REDDIT_INTERFACE = RedditInterface(PRAW_REDDIT)

# Handle if credentials are invalid
else:

    try:
        # Prompt for new valid credentials
        while True:
            MAIN_LOGGER.error(
                "The provided credentials are invalid. "
                "Please enter new valid credentials"
            )
            
            # Pause console logging while listening for input
            level = CONSOLE_HANDLER.level
            CONSOLE_HANDLER.setLevel(logging.CRITICAL)
    
            user_agent = input("Enter User Agent: ")
            client_id = input("Enter Client ID: ")
            client_secret = input("Enter Client Secret: ")
            username = input("Enter Username: ")
            password = input("Enter Password: ")

            reddit = praw.Reddit(
                user_agent=user_agent,
                client_id=client_id,
                client_secret=client_secret,
                username=username,
                password=password
            )

            # Resume console logging
            CONSOLE_HANDLER.setLevel(level)

            if __authenticated(reddit):
                REDDIT_INTERFACE = RedditInterface(
                    reddit
                )
                
                # Save new credentials to database
                newBotCredentials = BotCredentials(
                    user_agent, client_id,
                    client_secret, username,
                    password
                )
                newDatabaseConnection = DATABASE_CONNECTION_FACTORY \
                    .getConnection()
                try:
                    newBotCredentialsDAO = BotCredentialsDAO(
                        newDatabaseConnection
                    )
                    newBotCredentialsDAO.saveBotCredentials(newBotCredentials)

                # Handle if save operation fails
                except Exception as ex:
                    MAIN_LOGGER.error(
                        "Failed to save new bot credentials"
                        " to database. Error: {}".format(str(ex.args), exc_info=True)
                    )
                finally:
                    newDatabaseConnection.close()
                    newBotCredentials.clearCredentials()

                    # Resume console logging once authenticated
                    CONSOLE_HANDLER.setLevel(level)
                    break
                
    # Abort and quit application If shutdown
    # is requested mid-prompt
    except KeyboardInterrupt or EOFError:
        MAIN_LOGGER.warning(
            "Forced shut down requested."
            " Bot now shutting down"
        )
        sys.exit(1)


# Initializing the Programs Executor
MAIN_LOGGER.debug("Initializing the Programs Executor")

# Initializing the Program Runner
programRunnerIO = ProgramRunnerIO(
    CONFIG_PARSER, PROGRAM_RUNNER_LOGGER,
    DATABASE_CONNECTION_FACTORY
)
try:
    programRunner = ProgramRunner(
        programRunnerIO,
        REDDIT_INTERFACE
    )

# Handle if there is an error initializing the Program Runner
except InitializationError as ex:
    MAIN_LOGGER.critical(
        "A fatal error just occurred while initializing "
        "the bot application's program runner: Error(s): "
        + str(ex.args), exc_info=True
    )
    sys.exit(2)

# Setting up the Programs Executor
EXECUTOR = ThreadPoolExecutor()
programsExecutor = AsynchronousProgramsExecutor(
    PROGRAMS_EXECUTOR_LOGGER,
    EXECUTOR,
    programRunner
)
# -------------------------------------------------------------------------------


# Bot application commands
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

# Starting up the bot
def startBot(args=sys.argv):
    
    MAIN_LOGGER.info('Starting the bot ...')
    MAIN_LOGGER.debug('Running initial program commands')
    programsExecutor.executePrograms(INITIAL_PROGRAM_COMMANDS)
    MAIN_LOGGER.info('Bot is now running')
    
    try:
        try:
            # Retrieve additional instructions if present
            if len(args) > 1:

                try:
                    listen = int(args[1])  # Commnand listening setting

                    # Retrieve and execute bot command if present
                    if len(args) > 2:
                        botcommand = " ".join(args[2:])
                        __processBotCommand(botcommand)

                    # Check if command listening is set
                    if listen:
                        __startCommandListener()  # Start listening for commands

                # Handle if provided listen argument is invalid
                except ValueError:
                    MAIN_LOGGER.error(
                        "The provided 'listen' argument, \"{}\", is invalid. "
                        "The bot will therefore shutdown once all bot tasks"
                        " are completed.".format(args[1])
                    )
                    shutdownBot(True, 1)
            else:
                __startCommandListener()  # Start listening for commands
        # Handle forced shutdown request
        except KeyboardInterrupt:
            CONSOLE_HANDLER.setLevel(logging.DEBUG)  # Sloppy; will need cleaning-up
            MAIN_LOGGER.warning(
                'Forced bot shutdown requested. Please wait a bit wait while '
                'a graceful shutdown is attempted or press Ctrl+Break to '
                'exit immediately'
            )
            shutdownBot(True, 1)

        # Handle unknown exception while bot is running
        except Exception as er:
            MAIN_LOGGER.critical(
                "A fatal error just occurred while the bot was "
                "running. Please wait a bit wait while "
                "a graceful shutdown is attempted or press Ctrl+Break "
                "to exit immediately. Error(s): " + str(er.args),
                exc_info=True
            )
            shutdownBot(True, 2)

    # Handle forced shutdown request midway through graceful shutdown
    except KeyboardInterrupt:
        MAIN_LOGGER.warning(
            'Graceful shutdown aborted.'
        )
        shutdownBot(False, 2)


# Starting the bot command listener
def __startCommandListener():
    while True:
        level = CONSOLE_HANDLER.level
        # Disable console logging while bot is
        # listening for commands
        CONSOLE_HANDLER.setLevel(logging.CRITICAL)

        command = input('Enter bot command: ')

        # Re-enable console logging once command
        # entered
        CONSOLE_HANDLER.setLevel(level)

        __processBotCommand(command)


# Processing a bot command
def __processBotCommand(command):

    # For program command
    if command.startswith('run '):
        programsExecutor.executeProgram(command.split('run ', 1)[1])

    # For programs status request
    elif command == 'status':

        print('\nPrograms status:')
        # Printing all program statuses
        for program, task in programsExecutor.getPrograms().items():
            print('{}\t: {}'.format(
                program, 'DONE' if task.done() else 'RUNNING'
            ))
        print()

    # For shutdown command
    elif (
            command == 'shutdown' or
            command == 'quit' or
            command == 'exit'
    ):
        shutdownBot()

    else:
        MAIN_LOGGER.debug(
            "'{}' is not a valid bot command".format(command)
        )


# Shut down the bot
def shutdownBot(wait=True, shutdownExitCode=0):

    if wait:
        MAIN_LOGGER.info(
            'Shutting down the bot. Please wait a bit wait while '
            'remaining tasks are being finished off'
        )
        try:
            programsExecutor.shutdown(True)
            MAIN_LOGGER.info('Bot successfully shut down')
            sys.exit(shutdownExitCode)

        # Handle keyboard interrupt midway through graceful shutdown
        except KeyboardInterrupt:
            MAIN_LOGGER.warning(
                'Graceful shutdown aborted.'
            )
            MAIN_LOGGER.info('Bot shut down')
            sys.exit(2)
    else:
        programsExecutor.shutdown(False)
        MAIN_LOGGER.info('Bot shut down')
        sys.exit(shutdownExitCode)

# -------------------------------------------------------------------------------


# Let the games begin boysss
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
if __name__ == "__main__":
    startBot()
