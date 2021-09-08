# -*- coding: utf-8 -*
from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetailDAO \
    import StarSceneInfoSubmissionDetailDAO


class IndividualStarView:
    """
    Class to generate and hold the Stars Archive
    wiki "view" organized per individual star
    """

    __viewMarkdown: str
    __starSceneInfoSubmissionDetailDAO: StarSceneInfoSubmissionDetailDAO

    def __init__(
            self,
            starSceneInfoSubmissionDetailDAO:
            StarSceneInfoSubmissionDetailDAO
    ):
        self.__viewMarkdown = None
        self.__starSceneInfoSubmissionDetailDAO = starSceneInfoSubmissionDetailDAO

    @classmethod
    def __generateViewMarkdown(
            cls,
            starSceneInfoSubmissionDetailDAO:
            StarSceneInfoSubmissionDetailDAO
    ):
        """
        Utility method for generating the markdown
        for the view from provided data
        """

        starViewRecords = starSceneInfoSubmissionDetailDAO.retrieveAll()
        pageData = ''

        if len(starViewRecords) > 0:
            sceneInfoSubmission = starViewRecords[0].getSceneInfoSubmission
            # Generating markdown for each star
            pageData += (
                '## ' + starViewRecords[0].getStarName[0].upper() +
                '\n---\n\n'
            )
            pageData += (
                '### ' + starViewRecords[0].getStarName + '\n'
            )
            pageData += (
                '- [' + sceneInfoSubmission.getTitle + ']' +
                '(https://www.reddit.com/comments/' +
                sceneInfoSubmission.getSubmissionId + ')\n'
            )
            
            for index in range(1, len(starViewRecords) - 1):

                sceneInfoSubmission = starViewRecords[index] \
                    .getSceneInfoSubmission

                # Paragraphing once all of a star's individual
                # posts have been traversed
                if (
                    starViewRecords[index].getStarName !=
                    starViewRecords[index - 1].getStarName
                ):
                    # Creating a character heading to demarcate
                    # a change (if there is one) in the first letter 
                    # of the subsequent star names 
                    if (
                        starViewRecords[index].getStarName[0].upper() !=
                        starViewRecords[index - 1].getStarName[0].upper()
                    ):
                        pageData += (
                            '\n\n## ' + starViewRecords[index].getStarName[0].upper() +
                            '\n\n---\n'
                        )
                    pageData += ('\n\n### ' + starViewRecords[index].getStarName + '\n')

                pageData += (
                    '- [' + sceneInfoSubmission.getTitle + ']' +
                    '(https://www.reddit.com/comments/' +
                    sceneInfoSubmission.getSubmissionId + ')\n'
                )

        return pageData

    def updateViewMarkdown(self):
        """Update the view's markdown"""

        self.__viewMarkdown = self.__generateViewMarkdown(
            self.__starSceneInfoSubmissionDetailDAO
        )

    @property
    def getViewMarkdown(self):
        """Retrieve the view's markdown"""

        if self.__viewMarkdown is None:
            self.updateViewMarkdown()
        return self.__viewMarkdown
