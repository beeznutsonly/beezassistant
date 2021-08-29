# -*- coding: utf-8 -*-

import concurrent.futures
import json
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Dict, List

from botapplicationtools.programrunners.GenericProgramRunner \
    import GenericProgramRunner
from botapplicationtools.programsexecutors.ProgramsExecutor import \
    ProgramsExecutor
from botapplicationtools.programsexecutors.exceptions \
    .ProgramsExecutorInitializationError import \
    ProgramsExecutorInitializationError


class AsynchronousProgramsExecutor(ProgramsExecutor):
    """
    Class responsible for asynchronously executing
    multiple programs in different threads
    """

    __executor: ThreadPoolExecutor
    __programRunners: Dict[str, GenericProgramRunner]
    __executedPrograms: Dict[str, Future]

    def __init__(
            self,
            programRunners,
            configReader,
            executor=ThreadPoolExecutor()
    ):
        super().__init__()
        self.__executor = executor
        self.__programRunners = programRunners
        self.__initializeProgramsExecutor(configReader)

    def __initializeProgramsExecutor(self, configReader):
        """Initialize the programs executor"""

        self._programsExecutorLogger.debug('Initializing Programs Executor')

        try: 
            # Retrieving initial program commands
            self._programsExecutorLogger.debug(
                "Retrieving initial program commands"
            )
            initialProgramCommands = self.__getInitialProgramCommands(
                configReader
            )

            # Executing initial program commands 
            self._programsExecutorLogger.debug(
                "Executing initial program commands"
            )
            self.executePrograms(initialProgramCommands)
        
        # Handle in case the programs executor fails to initialize
        except ProgramsExecutorInitializationError as ex:
            self._programsExecutorLogger.critical(
                "A terminal error occurred while initializing the Programs "
                "Executor. Error(s): " + str(ex)
            )
            raise ex

        self.__isProgramsExecutorShutDown = False
        self._programsExecutorLogger.info(
            "Programs Executor initialized"
        )

    @staticmethod
    def __getInitialProgramCommands(configReader) \
            -> List[str]:
        """Retrieve initial program commands"""

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

    def executeProgram(self, programCommand):

        # Confirm if shut down first
        if self._informIfShutDown():
            return

        # Checking if there are duplicate running programs
        if programCommand in self.__executedPrograms.keys():
            if not self.__executedPrograms[programCommand].done():
                self._programsExecutorLogger.warning(
                    "Did not run the '{}' program command "
                    "because an identical command is"
                    " still running".format(programCommand)
                )
                return

        # Generating an asynchronous worker thread for the program
        try:
            task = self.__executor.submit(
                self.__processProgram,
                programCommand
            )
        except RuntimeError:
            self._programsExecutorLogger.error(
                "Failed to execute '{}' because the executor is "
                "shutting down or is shut down".format(programCommand)
            )
            return

        try:

            raise task.exception(0.1)

        # Add to running programs if task was started successfully
        except concurrent.futures.TimeoutError:

            self.__executedPrograms[programCommand] = task

        # Handle if provided program could not be parsed
        except ValueError as ex:
            self._programsExecutorLogger.error(
                "Did not run the '{}' program command "
                "because there was an error parsing the "
                "program command. Error(s): {}".format(
                    programCommand, str(ex.args)
                )
            )

    def executePrograms(self, programs):
        """Execute multiple programs"""

        # Confirm if shut down first
        if self._informIfShutDown():
            return

        for program in programs:
            self.executeProgram(program)

    def __processProgram(self, programCommand):
        """Synthesize the provided program"""

        programCommandBreakdown = programCommand.split()
        program = programCommandBreakdown[0]

        try:

            if program in self.__programRunners.keys():
                self._programsExecutorLogger.info(
                    "Running program '{}'".format(program)
                )
                self.__programRunners[program].run()

            # Raise error if provided program does not exist
            else:
                raise ValueError(
                    "Program '{}' is not recognized".format(program)
                )

        # Handle if provided program not found
        except ValueError as ex:
            raise ex

        # Handle if unexpected exception crashes a program
        except Exception as ex:
            self._programsExecutorLogger.error(
                "An unexpected error just caused the '{}' "
                "program to crash. Error: {}".format(
                    program, str(ex.args)
                ), exc_info=True
            )

    def getProgramStatuses(self):
        """Get the executed program statuses"""

        programStatuses = \
            {
                program: ("RUNNING" if not task.done() else "DONE")
                for (program, task) in self.__executedPrograms.items()
            }
        return programStatuses

    def shutDown(self, wait):
        """Shut down the programs executor"""

        super().shutDown()
        for programRunner in self.__programRunners.values():
            programRunner.shutDown()
        self.__executor.shutdown(wait)
        self._programsExecutorLogger.info(
            "Programs executor successfully shut down"
        )
