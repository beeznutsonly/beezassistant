from datetime import datetime, timezone

from botapplicationtools.programs.adminupdater.AdminUpdate import AdminUpdate


class FormattingTools:

    def __init__(
            self,
            wikiUpdateFormat: str,
            widgetUpdateFormat: str,
            dateFormat: str,
            maxWidgetLines: int,
            widgetFooter: str
    ):
        self.__wikiUpdateFormat = wikiUpdateFormat
        self.__widgetUpdateFormat = widgetUpdateFormat
        self.__dateFormat = dateFormat
        self.__maxWidgetLines = maxWidgetLines
        self.__widgetFooter = widgetFooter

    def getWikiUpdateMarkdown(self, adminUpdate: AdminUpdate) -> str:
        return self.__wikiUpdateFormat.format(
            timestamp=datetime.now(timezone.utc).strftime(
                self.__dateFormat
            ),
            heading=adminUpdate.getHeading,
            details=adminUpdate.getDetails
        )

    def getWidgetUpdateMarkdown(self, adminUpdate: AdminUpdate) -> str:
        return self.__widgetUpdateFormat.format(
            timestamp=datetime.now(timezone.utc).strftime(
                self.__dateFormat
            ),
            heading=adminUpdate.getHeading,
            details=adminUpdate.getDetails
        )

    @property
    def getMaxWidgetLines(self):
        return self.__maxWidgetLines

    @property
    def getWidgetFooter(self):
        return self.__widgetFooter
