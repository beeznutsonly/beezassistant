import logging
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta

from botapplicationtools.programrunners.ProgramRunner import ProgramRunner


class PostsManagerRunner(ProgramRunner):

    __programRunnerLogger = None
    __databaseConnectionFactory = None
    __prawReddit = None

    def __init__(
            self,
            databaseConnectionFactory,
            redditInterfaceFactory,
            configReader
    ):

        super(PostsManagerRunner, self).__init__()
        self.__programRunnerLogger = logging.getLogger('postsManager')
        self.__databaseConnectionFactory = databaseConnectionFactory
        self.__prawReddit = redditInterfaceFactory.getRedditInterface().getPrawReddit

    def run(self):
        try:
            postProcessExecutor = ThreadPoolExecutor()
            post1 = [
                'https://redgifs.com/watch/cooperativeadeptsiberiantiger',
                'Scene from *Charity Case* with **Lisey Sweet** and **Will Pounder**',
                ['porn', 'nsfw', 'lostinthemoment'],
                datetime(
                    2021,
                    9,
                    4,
                    13,
                    0,
                    0
                ).replace(
                    tzinfo=timezone.utc
                )
            ]
            post2 = [
                'https://redgifs.com/watch/cuteincrediblequoll',
                'Scene from *MILF Pact* with **Dana Vespoli** and **Lucas Frost**',
                ['nsfw', 'lostinthemoment'],
                datetime(
                    2021,
                    9,
                    5,
                    13,
                    0,
                    0
                ).replace(
                    tzinfo=timezone.utc
                )
            ]
            prawRedditInstance = self.__prawReddit
            self.__programRunnerLogger.info('Posts Manager is now running')
            for submission in prawRedditInstance.subreddit("romanticxxx").stream.submissions(
            ):
                if submission.url == post1[0]:
                    postProcessExecutor.submit(self.__processPost, submission, post1)
                elif submission.url == post2[0]:
                    postProcessExecutor.submit(self.__processPost, submission, post2)
                elif submission.url == post3[0]:
                    postProcessExecutor.submit(self.__processPost, submission, post3)
        except Exception as ex:
            self.__programRunnerLogger.critical('This is bad {}'.format(str(ex.args)), exc_info=True)

    # (To be refactored soon) Process Posts Manager Post
    def __processPost(self, submission, postArgs):
        self.__programRunnerLogger.info('Processing: ' + str(submission.title))
        if (
                datetime.now(tz=timezone.utc) <= (postArgs[3] + timedelta(
                            minutes=60
                        ))
        ):
            submission.reply(postArgs[1])
            for subreddit in postArgs[2]:
                time.sleep(600)
                if subreddit=='porn':
                    submission.crosspost(
                        subreddit='porn',
                        title='[/r/romanticxxx] {}'.format(
                            submission.title
                        )
                    )
                else:
                    submission.crosspost(
                        subreddit=subreddit
                    )
