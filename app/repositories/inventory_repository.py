from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.exceptions import SchemaNotReady
from app.repositories.base import BaseRepository


class InventoryRepository(BaseRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession], *, max_rows: int) -> None:
        super().__init__(session_factory, max_rows=max_rows)

    async def stock(self, restaurant_id: str) -> list[dict[str, object]]:
        raise SchemaNotReady("inventory tables are not connected")
