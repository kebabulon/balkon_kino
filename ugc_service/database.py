from datetime import datetime, timezone
from threading import RLock

from .models import UGCItem
from .exceptions import ReviewNotFoundError

class Database:
    def __init__(self):
        self.items = {}
        self._next_id = 1
        self.lock = RLock()

    def create(self, movie_id, kind, author, content=None, rating=None):
        now = datetime.now(timezone.utc)
        with self.lock:
            item = UGCItem(
                id=self._next_id,
                movie_id=movie_id,
                kind=kind,
                author=author,
                content=content,
                rating=rating,
                status="pending",
                moderation_note=None,
                created_at=now,
                updated_at=now,
            )
            self.items[item.id] = item
            self._next_id += 1
            return item

 
    def clear(self):
        with self.lock:
            self.items.clear()
            self._next_id = 1

engine = Database()

def close_db(error=None):
    pass
