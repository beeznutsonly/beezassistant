import time
from typing import List

from botapplicationtools.programs.adminupdater.AdminUpdate import AdminUpdate
from botapplicationtools.programs.adminupdater.AdminUpdateDAO import AdminUpdateDAO
from botapplicationtools.programs.adminupdater.FormattingTools import FormattingTools
from botapplicationtools.programs.adminupdater.RedditTools import RedditTools
from botapplicationtools.programs.programtools.programnatures.SimpleProgram import SimpleProgram


class AdminUpdater(SimpleProgram):
    """
    Program to automatically output,
    user-generated admin updates
    """

    def __init__(
            self,
            adminUpdateDAO: AdminUpdateDAO,
            redditTools: RedditTools,
            formattingTools: FormattingTools,
            stopCondition
    ):
        super().__init__()
        self.__adminUpdateDAO = adminUpdateDAO
        self.__redditTools = redditTools
        self.__formattingTools = formattingTools
        self.__stopCondition = stopCondition

    def execute(self, *args):

        # Program loop TODO: Decorate
        while not self.__stopCondition():
            pendingAdminUpdates = self.__adminUpdateDAO \
                .retrievePendingAdminUpdates()

            # Process if there are any pending updates
            if pendingAdminUpdates:
                self.__processAdminUpdates(
                    pendingAdminUpdates
                )
            time.sleep(1)

    def __processAdminUpdates(self, adminUpdates: List[AdminUpdate]):
        """Process pending admin updates"""

        # Local variable initialization
        adminUpdatesWiki = self.__redditTools.getAdminUpdatesWikiPage()
        adminUpdatesWidget = self.__redditTools.getAdminUpdatesWidget()

        newWikiPageItems = []
        newWidgetItems = []

        # Building the update markdowns for both the widget and wiki page

        for adminUpdate in adminUpdates:
            newWikiPageItems.append(
                self.__formattingTools.getWikiUpdateMarkdown(
                    adminUpdate
                )
            )
            newWidgetItems.append(
                self.__formattingTools.getWidgetUpdateMarkdown(
                    adminUpdate
                )
            )

        currentWikiPageMarkdown = adminUpdatesWiki.content_md
        currentWidgetMarkdown = adminUpdatesWidget.text

        newWikiPageItems.append(
            currentWikiPageMarkdown
        )
        # De-duplicating white space for more consistent processing
        minifiedCurrentWidgetMarkdown = currentWidgetMarkdown.replace(
            '\n\n', '\n'
        )
        newWidgetItems.extend(
            minifiedCurrentWidgetMarkdown
            .split('\n')
        )

        # Limit lines output to widget to specified threshold
        # if threshold is met
        if len(newWidgetItems) > self.__formattingTools.getMaxWidgetLines:
            newWidgetItems = newWidgetItems[
                             :self.__formattingTools.getMaxWidgetLines
                             ]
        newWidgetItems.append(self.__formattingTools.getWidgetFooter)

        # Outputting changes to the subreddit
        adminUpdatesWiki.edit(
            "\n\n".join(
                newWikiPageItems
            )
        )
        adminUpdatesWidget.mod.update(
            text="\n\n".join(
                newWidgetItems
            )
        )

        # Acknowledging successful processing of update
        self.__adminUpdateDAO.markCompleted(adminUpdates)
