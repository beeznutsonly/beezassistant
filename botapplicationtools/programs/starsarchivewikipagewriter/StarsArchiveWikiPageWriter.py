# -*- coding: utf-8 -*

from datetime import datetime, timezone
from typing import List

from praw.models import WikiPage

from botapplicationtools.programs.programtools.programnatures.SimpleProgram import SimpleProgram
from botapplicationtools.programs.starsarchivewikipagewriter.IndividualStarView import IndividualStarView


class StarsArchiveWikiPageWriter(SimpleProgram):
    """
    Program that archives Scene Info on a
    Stars Archive wiki page according to
    the provided StarViews
    """

    __starsArchiveWikiPage: WikiPage
    __starViews: List[IndividualStarView]

    def __init__(
            self,
            starsArchiveWikiPage: WikiPage,
            starViews: List[IndividualStarView]
    ):
        self.__starsArchiveWikiPage = starsArchiveWikiPage
        self.__starViews = starViews

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

        self.__starsArchiveWikiPage.edit(pageMarkdown)
