from dataclasses import dataclass
from datetime import datetime

@dataclass
class UGCItem:
    id: int
    movie_id: int
    kind: str
    author: str
    content: str | None
    rating: int | None
    status: str
    moderation_note: str | None
    created_at: datetime
    updated_at: datetime

class Base:
    pass
