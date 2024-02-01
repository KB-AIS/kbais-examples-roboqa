import abc
from typing import Generic, TypeVar

TCmd = TypeVar("TCmd")
TRes = TypeVar("TRes")


class UseCase(abc.ABC, Generic[TCmd, TRes]):

    @abc.abstractmethod
    async def execute(self, cmd: TCmd) -> TRes:
        raise NotImplementedError
