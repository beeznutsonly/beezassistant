from typing import Generator

from praw.models import Subreddit

from botapplicationtools.programs.programtools.programnatures.streamprocessingnature.StreamFactory import StreamFactory


class SimpleCommentStreamFactory(StreamFactory):
    """
    Class responsible for producing
    new Comment streams at request
    """

    def __init__(
            self,
            subreddit: Subreddit,
            pause_after: int = 0,
            skip_existing: bool = False
    ):
        super().__init__()
        self.__subreddit = subreddit
        self.__pause_after = pause_after
        self.__skip_existing = skip_existing

    def getNewStream(self) -> Generator:
        return self.__subreddit.stream.comments(
            pause_after=self.__pause_after,
            skip_existing=self.__skip_existing
        )
