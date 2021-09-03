from typing import List, Iterator

from praw import Reddit
from praw.models import Comment


class RedditTools:
    """Class holding Reddit Tools used by the Star Info Replyer"""

    __prawReddit: Reddit
    __commentStream: Iterator[Comment]
    __excludedUsers: List[str]

    def __init__(
            self,
            prawReddit: Reddit,
            subreddits: List[str],
            excludedUsers: List[str] = None
    ):
        self.__prawReddit = prawReddit
        self.__commentStream = prawReddit.subreddit(
            "+".join(subreddits)
        ).stream.comments(pause_after=0)
        self.__excludedUsers = excludedUsers

    @property
    def getPrawReddit(self):
        return self.__prawReddit

    @property
    def getCommentStream(self):
        return self.__commentStream

    @property
    def getExcludedUsers(self):
        return self.__excludedUsers
