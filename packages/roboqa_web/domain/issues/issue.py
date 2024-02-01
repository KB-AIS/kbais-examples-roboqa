from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class Issue(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    title: str = Field()
    author: Optional[str] = Field(default=None, serialization_alias='authorName')
    content: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)
