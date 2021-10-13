from praw.models import Submission

from botapplicationtools.programs.programtools.generaltools.SimpleSubmission \
    import SimpleSubmission


class SceneInfoSubmission(SimpleSubmission):
    """
    Class encapsulating a scene info submission
    """

    __title: str
    __movieName: str
    __timeCreated: int

    def __init__(
            self,
            submissionId: str,
            title: str,
            timeCreated: int,
            movieName: str = None
    ):

        super().__init__(submissionId)
        self.__title = title
        self.__timeCreated = timeCreated
        self.__movieName = movieName

    @property
    def getTitle(self):
        return self.__title

    @property
    def getTimeCreated(self):
        return self.__timeCreated

    @property
    def getMovieName(self):
        return self.__movieName

    @classmethod
    def getSceneInfoSubmissionFromDetails(
            cls,
            submissionId: str,
            title: str,
            timeCreated: int
    ):
        """
        Generates a new SceneInfoSubmission object
        from the SceneInfoSubmission details
        """

        return SceneInfoSubmission(
            submissionId,
            title,
            timeCreated
        )

    @classmethod
    def getSceneInfoSubmissionFromPrawSubmission(
            cls, prawSubmission: Submission
    ):
        """
        Generates a new SceneInfoSubmission object
        from the provided PRAW submission
        """
        return SceneInfoSubmission(
            prawSubmission.id,
            prawSubmission.title,
            prawSubmission.created_utc
        )
