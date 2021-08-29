# -*- coding: utf-8 -*

"""
Program responsible for archiving scene info
both to provided storage and to a stars archive
wiki page
"""

from botapplicationtools.programs.sceneinfostoragearchiver \
    import SceneInfoStorageArchiver
from botapplicationtools.programs.starsarchivewikipagewriter \
    import StarsArchiveWikiPageWriter


def execute(storageArchiverTools, wikiPageWriterTools):
    """Execute the program"""

    SceneInfoStorageArchiver.execute(
        storageArchiverTools.getPushShiftAPI,
        storageArchiverTools.getSubredditSearchParameters,
        storageArchiverTools.getSceneInfoSubmissionsWithSceneInfoStorage
    )

    StarsArchiveWikiPageWriter.execute(
        wikiPageWriterTools.getWikiPage,
        wikiPageWriterTools.getStarViews
    )
