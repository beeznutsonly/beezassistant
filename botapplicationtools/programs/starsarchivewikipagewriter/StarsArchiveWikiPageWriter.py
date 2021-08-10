# -*- coding: utf-8 -*

"""
Class that encapsulates a Stars Archive
Wiki Page's writer/updater
"""

from datetime import datetime, timezone


class StarsArchiveWikiPageWriter:

    __starsArchiveWikiPage = None
    __starViews = None

    def __init__(self, starsArchiveWikiPage, starViews):
        self.__starsArchiveWikiPage = starsArchiveWikiPage
        self.__starViews = starViews

    # Writing all starviews to stars archive wiki page
    def writeToWiki(self, starViews = None):
        pageMarkdown = '# **Star Archive**\n\n'
        pageMarkdown += (
                    '_Automatically generated by u/beezassistant on ' +
                    datetime.now(timezone.utc).strftime(
                        "%b %d %Y at %H:%M %z"
                    ) + '_\n\n'
        )
        
        for starView in (
                self.__starViews if starViews is None else starViews
        ):
            pageMarkdown += (starView.getViewMarkdown() + '\n\n')
        
        self.__starsArchiveWikiPage.edit(pageMarkdown)
