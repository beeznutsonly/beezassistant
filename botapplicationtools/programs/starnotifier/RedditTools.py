from praw import Reddit


class RedditTools:

    __prawReddit: Reddit
    __commentStream = None

    def __init__(
            self,
            prawReddit: Reddit,
            subreddit: str
    ):
        self.__prawReddit = prawReddit
        self.__commentStream = prawReddit.subreddit(
            subreddit
        ).stream.comments(
            skip_existing=True,
            pause_after=0
        )

    @property
    def getPrawReddit(self):
        return self.__prawReddit

    @property
    def getCommentStream(self):
        return self.__commentStream
