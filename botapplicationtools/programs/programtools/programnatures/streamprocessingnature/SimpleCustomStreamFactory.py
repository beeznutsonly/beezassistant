from typing import Generator, Callable

from praw.models import ListingGenerator
from praw.models.util import stream_generator

from botapplicationtools.programs.programtools.programnatures.streamprocessingnature.StreamFactory import StreamFactory


class SimpleCustomStreamFactory(StreamFactory):
    """
    Class responsible for producing new
    stream of custom Reddit objects according to
    the provided Listing Generator
    """

    def __init__(
            self,
            listingGeneratorCallback: Callable[..., ListingGenerator],
            pause_after: int = 0,
            skip_existing: bool = False
    ):
        super().__init__()
        self.__listingGeneratorCallback = listingGeneratorCallback
        self.__pause_after = pause_after
        self.__skip_existing = skip_existing

    def getNewStream(self) -> Generator:
        return stream_generator(
            self.__listingGeneratorCallback(),
            pause_after=self.__pause_after,
            skip_existing=self.__skip_existing
        )
