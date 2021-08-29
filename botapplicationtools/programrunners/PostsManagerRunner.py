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
            redditInterface,
            configReader
    ):

        super(PostsManagerRunner, self).__init__()
        self.__programRunnerLogger = logging.getLogger('postsManager')
        self.__databaseConnectionFactory = databaseConnectionFactory
        self.__prawReddit = redditInterface.getPrawReddit

    def run(self):
        try:
            postProcessExecutor = ThreadPoolExecutor()
            post1 = [
                'https://redgifs.com/watch/illfatedmilkyturtle',
                'Clip from [Husband Gets Seconds And Cums Quick]'
                '(https://www.pornhub.com/view_video.php?viewkey=ph5d0590feca9e6) '
                'by [Jane Dro](https://www.pornhub.com/model/jane-dro)',
                ['nsfw', 'forgottopullout', 'lostinthemoment'],
                datetime(
                    2021,
                    8,
                    28,
                    13,
                    0,
                    0
                ).replace(
                    tzinfo=timezone.utc
                )
            ]
            post2 = [
                'https://redgifs.com/watch/aridcraftybufeo',
                'Scene from *Lesbian Adventures: Strap-On Specialists 15* with **Lena Paul** and **Sinn Sage**',
                ['nsfw', 'lesbians', 'lenapaul'],
                datetime(
                    2021,
                    8,
                    29,
                    13,
                    0,
                    0
                ).replace(
                    tzinfo=timezone.utc
                )
            ]
            post3 = [
                'https://redgifs.com/watch/ethicalstarkhoneycreeper',
                'Scene from *Raw 33* with **Abella Danger** and **Manuel Ferrara**',
                ['nsfw', 'abelladanger', 'lostinthemoment'],
                datetime(
                    2021,
                    8,
                    30,
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
            submission.crosspost(
                subreddit='porn',
                title='[/r/romanticxxx] {}'.format(
                    submission.title
                )
            )
            for subreddit in postArgs[2]:
                time.sleep(600)
                submission.crosspost(
                    subreddit=subreddit
                )
