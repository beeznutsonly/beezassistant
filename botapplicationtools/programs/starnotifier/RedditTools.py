from praw import Reddit

from botapplicationtools.programs.programtools.programnatures.streamprocessingnature.SimpleCommentStreamFactory import \
    SimpleCommentStreamFactory


class RedditTools:
    """
    Class holding Reddit tools to be used
    by the Star Notifier
    """

    def __init__(
            self,
            prawReddit: Reddit,
            subreddit: str
    ):
        self.__prawReddit = prawReddit
        self.__commentStreamFactory = SimpleCommentStreamFactory(
            prawReddit.subreddit(
                subreddit
            ),
            skip_existing=True
        )

    @property
    def getPrawReddit(self):
        return self.__prawReddit

    @property
    def getCommentStreamFactory(self):
        return self.__commentStreamFactory
