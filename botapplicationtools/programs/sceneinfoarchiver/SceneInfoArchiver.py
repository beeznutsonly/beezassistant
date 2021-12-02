# -*- coding: utf-8 -*

from botapplicationtools.programs.programtools.programnatures.SimpleProgram import SimpleProgram
from botapplicationtools.programs.sceneinfoarchiver.SceneInfoStorageArchiverTools import SceneInfoStorageArchiverTools
from botapplicationtools.programs.sceneinfoarchiver.StarsArchiveWikiPageWriterTools import \
    StarsArchiveWikiPageWriterTools
from botapplicationtools.programs.sceneinfostoragearchiver.SceneInfoStorageArchiver \
    import SceneInfoStorageArchiver
from botapplicationtools.programs.starsarchivewikipagewriter.StarsArchiveWikiPageWriter \
    import StarsArchiveWikiPageWriter


class SceneInfoArchiver(SimpleProgram):
    """
    Program responsible for archiving scene info
    both to provided storage and to a stars archive
    wiki page
    """

    def __init__(
            self,
            storageArchiverTools: SceneInfoStorageArchiverTools,
            wikiPageWriterTools: StarsArchiveWikiPageWriterTools
    ):
        self.__storageArchiverTools = storageArchiverTools
        self.__wikiPageWriterTools = wikiPageWriterTools

    def execute(self):

        storageArchiverTools = self.__storageArchiverTools
        wikiPageWriterTools = self.__wikiPageWriterTools

        sceneInfoStorageArchiver = SceneInfoStorageArchiver(
            storageArchiverTools.getPushShiftAPI,
            storageArchiverTools.getSubredditSearchParameters,
            storageArchiverTools.getSceneInfoSubmissionsWithSceneInfoStorage
        )
        sceneInfoStorageArchiver.execute()

        starsArchiveWikiPageWriter = StarsArchiveWikiPageWriter(
            wikiPageWriterTools.getWikiPage,
            wikiPageWriterTools.getStarViews
        )
        starsArchiveWikiPageWriter.execute()
