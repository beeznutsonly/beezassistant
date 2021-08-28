import praw.models
from typing import List

from botapplicationtools.programs.starsarchivewikipagewriter.IndividualStarView import IndividualStarView


class StarsArchiveWikiPageWriterTools:

    __wikiPage: praw.models.WikiPage
    # TODO: Replace IndividualStarView generic with StarView
    __starViews: List[IndividualStarView]

    def __init__(self, wikiPage, starViews):
        self.__wikiPage = wikiPage
        self.__starViews = starViews

    def getWikiPage(self):
        return self.__wikiPage

    def getStarViews(self):
        return self.__starViews
