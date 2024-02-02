from abc import ABC, abstractmethod


class IssueSender(ABC):

    @abstractmethod
    def registered(self, issue_id: str) -> None:
        raise NotImplementedError
