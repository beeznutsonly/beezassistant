from botapplicationtools.programs.starsarchivewikipagewriter.IndividualStarView import IndividualStarView
from botapplicationtools.programs.starsarchivewikipagewriter.IndividualStarViewDAO import IndividualStarViewDAO


def getStarView(databaseConnection, starViewArgument):
    if starViewArgument == 'individual':
        return IndividualStarView(
            IndividualStarViewDAO(
                databaseConnection
            )
        )


def getStarViews(databaseConnection, starViewArguments):
    starViewObjects = []
    for starViewArgument in (
            [] if starViewArguments is None else starViewArguments
    ):
        starViewObject = getStarView(databaseConnection, starViewArgument)
        print(starViewObject)
        if starViewObject is not None:
            starViewObjects.append(starViewObject)

    return starViewObjects
