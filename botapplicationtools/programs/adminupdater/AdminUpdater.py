import time
from typing import List

from praw.models import WikiPage, TextArea

from botapplicationtools.programs.adminupdater.AdminUpdate import AdminUpdate
from botapplicationtools.programs.adminupdater.AdminUpdateDAO import AdminUpdateDAO
from botapplicationtools.programs.adminupdater.FormattingTools import FormattingTools
from botapplicationtools.programs.programtools.programnatures.SimpleProgram import SimpleProgram


class AdminUpdater(SimpleProgram):

    def __init__(
            self,
            adminUpdateDAO: AdminUpdateDAO,
            adminUpdateWiki: WikiPage,
            adminUpdateWidget: TextArea,
            formattingTools: FormattingTools,
            stopCondition
    ):
        super().__init__()
        self.__adminUpdateDAO = adminUpdateDAO
        self.__adminUpdateWiki = adminUpdateWiki
        self.__adminUpdateWidget = adminUpdateWidget
        self.__formattingTools = formattingTools
        self.__stopCondition = stopCondition

    def execute(self, *args):

        while not self.__stopCondition():
            pendingAdminUpdates = self.__adminUpdateDAO \
                .retrievePendingAdminUpdates()
            self.__processAdminUpdates(
                pendingAdminUpdates
            )
            time.sleep(1)

    def __processAdminUpdates(self, adminUpdates: List[AdminUpdate]):

        newWikiPageItems = []
        newWidgetItems = []

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

        currentWikiPageMarkdown = self.__adminUpdateWiki.content_md
        currentWidgetMarkdown = self.__adminUpdateWidget.text

        newWikiPageItems.append(
            currentWikiPageMarkdown
        )
        minifiedCurrentWidgetMarkdown = currentWidgetMarkdown.replace(
            '\n\n', '\n'
        )
        newWidgetItems.extend(
            minifiedCurrentWidgetMarkdown
            .split('\n')
        )
        if len(newWidgetItems) > self.__formattingTools.getMaxWidgetLines:
            newWidgetItems = newWidgetItems[
                             :self.__formattingTools.getMaxWidgetLines
                             ]
        newWidgetItems.append(self.__formattingTools.getWidgetFooter)

        self.__adminUpdateWiki.edit(
            "\n\n".join(
                newWikiPageItems
            )
        )
        self.__adminUpdateWidget.mod.update(
            text="\n\n".join(
                newWidgetItems
            )
        )
        
        self.__adminUpdateDAO.markCompleted(adminUpdates)
