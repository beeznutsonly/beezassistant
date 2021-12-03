from praw.models import Subreddit, WikiPage, TextArea


class RedditTools:
    """
    Class holding Reddit resources
    required by the Admin Updater
    """

    def __init__(
            self,
            subreddit: Subreddit,
            wikiPageName: str,
            widgetId: str
    ):

        self.__subreddit = subreddit
        self.__wikiPageName = wikiPageName
        self.__widgetId = widgetId

    def getAdminUpdatesWikiPage(self) -> WikiPage:
        """Retrieve the current admin updates wiki page"""

        return self.__subreddit.wiki[self.__wikiPageName]

    def getAdminUpdatesWidget(self) -> TextArea:
        """Retrieve the current admin updates sidebar widget"""

        return self.__subreddit.widgets.items[
            self.__widgetId
        ]
