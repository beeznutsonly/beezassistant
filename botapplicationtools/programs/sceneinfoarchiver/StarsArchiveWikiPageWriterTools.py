# -*- coding: utf-8 -*

import praw.models
from typing import List

from botapplicationtools.programs.starsarchivewikipagewriter \
    .IndividualStarView import IndividualStarView


class StarsArchiveWikiPageWriterTools:
    """
    Class holding tools required by the stars archive wiki
    page writer program
    """

    __wikiPage: praw.models.WikiPage
    # TODO: Replace IndividualStarView generic with StarView
    __starViews: List[IndividualStarView]

    def __init__(self, wikiPage, starViews):
        self.__wikiPage = wikiPage
        self.__starViews = starViews

    @property
    def getWikiPage(self):
        return self.__wikiPage

    @property
    def getStarViews(self):
        return self.__starViews
