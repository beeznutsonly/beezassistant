# -*- coding: utf-8 -*

from abc import ABC, abstractmethod

from botapplicationtools.databasetools.daos.DAO import DAO

from typing import TypeVar, Generic

T = TypeVar('T')


class ReadOnlyDAO(ABC, DAO, Generic[T]):
    """Class representing a read-only DAO"""

    @abstractmethod
    def retrieve(self, *args) -> T:
        """Retrieve object associated with the DAO"""

        raise NotImplementedError
