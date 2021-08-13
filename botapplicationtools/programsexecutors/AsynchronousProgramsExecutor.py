# -*- coding: utf-8 -*-

"""
Class responsible for asynchronously executing multiple programs
"""

from botapplicationtools.programsexecutors.exceptions.ProgramsExecutorInitializationError import ProgramsExecutorInitializationError
import concurrent.futures
import json
import logging
from concurrent.futures import ThreadPoolExecutor

from praw import config


class AsynchronousProgramsExecutor:

    __isProgramsExecutorShutDown = None

    __programsExecutorLogger: logging.Logger
    __executor = None
    __programRunner = None
    __programs = None

    def __init__(
            self,
            programRunner,
            configReader,
            executor=ThreadPoolExecutor(),
            programs={}
    ):
        self.__executor = executor
        self.__programRunner = programRunner
        self.__programs = programs
        self.__initializeProgramsExecutor(configReader)
        

    # Initialize the programs executor
    def __initializeProgramsExecutor(self, configReader):        
    
        # Setting up the Programs Executor logger
        self.__programsExecutorLogger = logging.getLogger("programsExecutor")    
        
        try: 
            # Retrieving initial program commands
            self.__programsExecutorLogger.debug(
                "Retrieving initial program commands"
            )
            initialProgramCommands = self.__getInitialProgramCommands(
                configReader
            )

            # Executing initial program commands 
            self.__programsExecutorLogger.debug(
                "Executing initial program commands"
            )
            self.executePrograms(initialProgramCommands)
        
        # Handle in case the programs executor fails to initialize
        except ProgramsExecutorInitializationError as ex:
            self.__programsExecutorLogger.critical(
                "A terminal error occurred while initializing the Programs "
                "Executor. Error(s): " + str(ex)
            )
            raise ex

        self.__isProgramsExecutorShutDown = False
        self.__programsExecutorLogger.info(
            "Programs Executor initialized"
        )

    # Retrieve initial program commands
    def __getInitialProgramCommands(self, configReader):

        try:
            # Initial program commands
            initialProgramCommands = json.loads(configReader.get(
                'ProgramsExecutor', 'initialprogramcommands'
            ))

        # Handle when there is a problem parsing the config file
        except configReader.Error or json.JSONDecodeError as ex:
            raise ProgramsExecutorInitializationError(
                "An error occurred while parsing the "
                "configuration file for the Programs Executor's "
                "initial program commands.", ex
            )

        return initialProgramCommands

    # Execute a single program
    def executeProgram(self, program):

        # Confirm if shut down first
        if self.__informIfShutdown():
            return

        # Checking if there are duplicate running programs
        if program in self.__programs.keys():
            if not self.__programs[program].done():
                self.__programsExecutorLogger.warning(
                    "Did not run the '{}' program command "
                    "because an identical command is"
                    " still running".format(program)
                )
                return

        # Generating an asynchronous task for the program
        task = self.__executor.submit(
            self.__processProgram,
            program
        )

        try:

            raise task.exception(0.1)

        # Add to running programs if task was started successfully
        except concurrent.futures.TimeoutError:

            self.__programs[program] = task

        # Handle if provided program could not be parsed
        except ValueError as ex:
            self.__programsExecutorLogger.error(
                "Did not run the '{}' program command "
                "because there was an error parsing the "
                "program command. Error(s): {}".format(
                    program, str(ex.args)
                )
            )

    # Execute multiple programs
    def executePrograms(self, programs):

        # Confirm if shut down first
        if self.__informIfShutdown():
            return

        for program in programs:
            self.executeProgram(program)

    # Synthesize the provided program
    def __processProgram(self, programCommand):

        programCommandBreakdown = programCommand.split()
        program = programCommandBreakdown[0]

        # Scene Info Archiver program
        if program == 'sceneinfoarchiver':
            self.__programsExecutorLogger.info(
                "Running program '{}'".format(program)
            )
            self.__programRunner.runSceneInfoArchiver()

        # Stars Archive Wiki Page Writer program
        elif program == 'starsarchivewikipagewriter':
            self.__programsExecutorLogger.info(
                "Running program '{}'".format(program)
            )
            self.__programRunner.runStarsArchiveWikiPageWriter()

        # Raise error if provided program does not exist
        else:
            raise ValueError(
                "Program '{}' is not recognized".format(program)
            )

    # Get the asynchronous program statuses
    def getProgramStatuses(self):
        programStatuses = \
            {
                program: ("RUNNING" if not task.done() else "DONE")
                for (program, task) in self.__programs.items()
            }
        return programStatuses

    def __informIfShutdown(self):
        if self.__isProgramsExecutorShutDown:
            self.__programsExecutorLogger.warning(
                "The programs executor cannot execute any more programs "
                "after it has been shut down"
            )

    # Shut down the programs executor
    def shutdown(self, wait):
        self.__isProgramsExecutorShutDown = True
        self.__programRunner.shutdown()
        self.__executor.shutdown(wait)
        self.__programsExecutorLogger.info(
            "Programs executor successfully shut down"
        )

    # Check if Programs Executor is shut down
    def isShutDown(self):
        return self.__isProgramsExecutorShutDown 
