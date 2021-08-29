# -*- coding: utf-8 -*

"""Factory module for StarViews"""

from botapplicationtools.programs.starsarchivewikipagewriter \
    .IndividualStarView import IndividualStarView
from botapplicationtools.programs.starsarchivewikipagewriter \
    .IndividualStarViewDAO import IndividualStarViewDAO


def getStarView(databaseConnection, starViewArgument):
    """
    Retrieve a StarView as per the provided argument
    """

    if starViewArgument == 'individual':
        return IndividualStarView(
            IndividualStarViewDAO(
                databaseConnection
            )
        )


def getStarViews(databaseConnection, starViewArguments):
    """
    Retrieve multiple StarViews as per the provided arguments
    """

    starViewObjects = []
    for starViewArgument in (
            [] if starViewArguments is None else starViewArguments
    ):
        starViewObject = getStarView(databaseConnection, starViewArgument)
        if starViewObject is not None:
            starViewObjects.append(starViewObject)

    return starViewObjects
