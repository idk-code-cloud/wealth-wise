from abc import ABC, abstractmethod
from typing import Optional, List


class BaseRepository[T](ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> Optional[List[T]]:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def exists_by_id(self, id: int) -> bool:
        raise NotImplementedError
