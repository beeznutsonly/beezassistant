from typing import List, Callable

from botapplicationtools.programs.adminupdater.AdminUpdate import AdminUpdate
from botapplicationtools.programs.adminupdater.AdminUpdateDAO import AdminUpdateDAO
from botapplicationtools.programs.adminupdater.FormattingTools import FormattingTools
from botapplicationtools.programs.adminupdater.RedditTools import RedditTools
from botapplicationtools.programs.programtools.generaltools.Decorators import consumestransientapierrors
from botapplicationtools.programs.programtools.programnatures.RecurringProgramNature import RecurringProgramNature


class AdminUpdater(RecurringProgramNature):
    """
    Program to automatically output,
    user-generated admin updates
    """

    PROGRAM_NAME: str = "Admin Updater"

    def __init__(
            self,
            adminUpdateDAO: AdminUpdateDAO,
            redditTools: RedditTools,
            formattingTools: FormattingTools,
            stopCondition: Callable[..., bool],
            cooldown: float = 1
    ):
        super().__init__(
            AdminUpdater.PROGRAM_NAME,
            stopCondition,
            cooldown
        )
        self.__adminUpdateDAO = adminUpdateDAO
        self.__redditTools = redditTools
        self.__formattingTools = formattingTools

    def _runNatureCore(self, *args, **kwargs):

        pendingAdminUpdates = self.__adminUpdateDAO \
            .retrievePendingAdminUpdates()

        # Process if there are any pending updates
        if pendingAdminUpdates:
            self.__processAdminUpdates(
                pendingAdminUpdates
            )

    @consumestransientapierrors
    def __processAdminUpdates(self, adminUpdates: List[AdminUpdate]):
        """Process pending admin updates"""

        self._programLogger.debug(
            "Processing new admin updates"
        )

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
        # if threshold is exceeded
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
        self._programLogger.debug(
            "Admin updates successfully pushed to wiki"
        )

        adminUpdatesWidget.mod.update(
            text="\n\n".join(
                newWidgetItems
            )
        )
        self._programLogger.debug(
            "Admin updates successfully pushed to widget"
        )

        # Acknowledging successful processing of update
        self.__adminUpdateDAO.markCompleted(adminUpdates)
        self._programLogger.debug(
            "Completion of admin updates successfully acknowledged"
        )
