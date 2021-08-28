from botapplicationtools.programs.sceneinfostoragearchiver import SceneInfoStorageArchiver
from botapplicationtools.programs.starsarchivewikipagewriter import StarsArchiveWikiPageWriter


def execute(storageArchiverTools, wikiPageWriterTools):

    SceneInfoStorageArchiver.execute(
        storageArchiverTools.getPushShiftAPI(),
        storageArchiverTools.getSubredditSearchParameters(),
        storageArchiverTools.getSceneInfoSubmissionsWithSceneInfoStorage()
    )

    StarsArchiveWikiPageWriter.execute(
        wikiPageWriterTools.getWikiPage(),
        wikiPageWriterTools.getStarViews()
    )
