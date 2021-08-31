# -*- coding: utf-8 -*

from abc import abstractmethod, ABC

from botapplicationtools.databasetools.daos.DAO import DAO

from typing import TypeVar, Generic

T = TypeVar('T')


class WriteOnlyDAO(ABC, DAO, Generic[T]):
    """Class representing a write-only DAO"""

    @abstractmethod
    def add(self, obj: T):
        """Add provided object to storage"""

        raise NotImplementedError
