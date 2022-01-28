from typing import List

from praw import Reddit

from botapplicationtools.programs.programtools.programnatures.streamprocessingnature.SimpleCommentStreamFactory import \
    SimpleCommentStreamFactory


class RedditTools:
    """Class holding Reddit Tools used by the Star Info Replyer"""

    def __init__(
            self,
            prawReddit: Reddit,
            subreddits: List[str],
            excludedUsers: List[str] = None
    ):
        self.__prawReddit = prawReddit
        self.__commentStreamFactory = SimpleCommentStreamFactory(
            prawReddit.subreddit(
                "+".join(subreddits)
            )
        )
        self.__excludedUsers = excludedUsers

    @property
    def getPrawReddit(self):
        return self.__prawReddit

    @property
    def getCommentStreamFactory(self):
        return self.__commentStreamFactory

    @property
    def getExcludedUsers(self):
        return self.__excludedUsers
