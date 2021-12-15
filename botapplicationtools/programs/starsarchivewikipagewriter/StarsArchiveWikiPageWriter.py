# -*- coding: utf-8 -*

from datetime import datetime, timezone
from typing import List

from praw.models import WikiPage

from botapplicationtools.programs.programtools.generaltools.Decorators import consumestransientapierrors
from botapplicationtools.programs.programtools.programnatures.SimpleProgram import SimpleProgram
from botapplicationtools.programs.starsarchivewikipagewriter.IndividualStarView import IndividualStarView


class StarsArchiveWikiPageWriter(SimpleProgram):
    """
    Program that archives Scene Info on a
    Stars Archive wiki page according to
    the provided StarViews
    """

    PROGRAM_NAME: str = "Stars Archive Wiki Page Writer"

    def __init__(
            self,
            starsArchiveWikiPage: WikiPage,
            starViews: List[IndividualStarView]
    ):
        super().__init__(StarsArchiveWikiPageWriter.PROGRAM_NAME)
        self.__starsArchiveWikiPage = starsArchiveWikiPage
        self.__starViews = starViews

    @consumestransientapierrors
    def execute(self):
        """Execute the program"""

        pageMarkdown = '# **Stars Archive**\n\n'
        pageMarkdown += (
                    '_Automatically generated on ' +
                    datetime.now(timezone.utc).strftime(
                        "%b %d %Y at %H:%M UTC"
                    ) + '_\n\n'
        )

        for starView in self.__starViews:
            pageMarkdown += (starView.getViewMarkdown + '\n\n')

        self._programLogger.debug(
            "Writing generated markdown to wiki page"
        )
        self.__starsArchiveWikiPage.edit(pageMarkdown)
        self._programLogger.debug(
            "Stars Archive wiki page successfully updated"
        )
