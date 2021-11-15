from abc import ABC, abstractmethod

from praw.models import Message


class CommandProcessor(ABC):
    """
    Class encapsulating objects responsible for
    processing user bot requests/commands
    """

    @abstractmethod
    def processMessage(self, message: Message, *args, **kwargs):
        """Process message command"""
        raise NotImplementedError()
