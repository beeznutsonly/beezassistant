# -*- coding: utf-8 -*

"""
Class to generate and hold the Stars Archive
wiki "view" organized per individual star
"""


class IndividualStarView:

    __viewMarkdown = None
    __individualStarViewDAO = None

    def __init__(self, individualStarViewDAO):
        self.__individualStarViewDAO = individualStarViewDAO

    # Utility method for generating the markdown
    # for the view from provided data
    @classmethod
    def __generateViewMarkdown(cls, individualStarViewDAO):
        starViewRecords = individualStarViewDAO.getIndividualStarViewRecords()
        pageData = ''

        if len(starViewRecords) > 0:
            # Generating markdown for each star
            pageData += (
                '## ' + starViewRecords[0].getStar()[0].upper() + 
                '\n---\n\n'
            )
            pageData += (
                '### ' + starViewRecords[0].getStar() + '\n'
            )
            pageData += (
                '- [' + starViewRecords[0].getTitle() + ']' + 
                '(https://www.reddit.com/comments/' +
                starViewRecords[0].getSubmissionId() + ')\n'
            )
            
            for index in range(1, len(starViewRecords) - 1):
                # Paragraphing once all of a star's individual
                # posts have been traversed
                if (
                    starViewRecords[index].getStar() != 
                    starViewRecords[index - 1].getStar()
                ):
                    # Creating a character heading to demarcate
                    # a change (if there is one) in the first letter 
                    # of the subsequent star names 
                    if (
                        starViewRecords[index].getStar()[0].upper() != 
                        starViewRecords[index - 1].getStar()[0].upper()
                    ):
                        pageData += (
                            '\n\n## ' + starViewRecords[index].getStar()[0].upper() +
                            '\n\n---\n'
                        )
                    pageData += ('\n\n### ' + starViewRecords[index].getStar() + '\n')

                pageData += (
                    '- [' + starViewRecords[index].getTitle() + ']' +
                    '(https://www.reddit.com/comments/' +
                    starViewRecords[index].getSubmissionId() + ')\n'
                )

        return pageData

    # Update the view's markdown
    def updateViewMarkdown(self):
        self.__viewMarkdown = self.__generateViewMarkdown(
            self.__individualStarViewDAO
        )

    # Retrieve the view's markdown
    def getViewMarkdown(self):
        if self.__viewMarkdown is None:
            self.__viewMarkdown = self.__generateViewMarkdown(
                self.__individualStarViewDAO
            )
        return self.__viewMarkdown
