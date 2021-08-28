from abc import ABC, abstractmethod


class GenericProgramRunner(ABC):

    _isProgramRunnerShutDown: bool

    def __init__(self):
        self._isProgramRunnerShutDown = False

    @abstractmethod
    def run(self):
        raise NotImplementedError()

    def isShutDown(self):
        return self._isProgramRunnerShutDown

    def shutDown(self):
        self._isProgramRunnerShutDown = True
