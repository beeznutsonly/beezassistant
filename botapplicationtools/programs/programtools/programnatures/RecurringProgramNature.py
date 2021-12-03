import time
from abc import abstractmethod, ABC
from typing import Callable

from botapplicationtools.programs.programtools.programnatures.SimpleProgram import SimpleProgram


class RecurringProgramNature(SimpleProgram, ABC):
    """Class encapsulating a looping program nature"""

    def __init__(
            self,
            stopCondition: Callable[..., bool],
            cooldown: float = 0
    ):
        self._stopCondition = stopCondition
        self.__cooldown = cooldown

    def execute(self, *args, **kwargs):
        while not self._stopCondition():
            self._runNatureCore(*args, **kwargs)
            if self.__cooldown and self.__cooldown > 0:
                time.sleep(self.__cooldown)

    @abstractmethod
    def _runNatureCore(self, *args, **kwargs):
        """Run core program"""

        raise NotImplementedError()
