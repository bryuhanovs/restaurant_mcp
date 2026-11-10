from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.exceptions import SchemaNotReady
from app.repositories.base import BaseRepository


class WriteOffsRepository(BaseRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession], *, max_rows: int) -> None:
        super().__init__(session_factory, max_rows=max_rows)

    async def write_offs(
        self,
        restaurant_id: str,
        date_from: date,
        date_to: date,
    ) -> list[dict[str, object]]:
        raise SchemaNotReady("write-off tables are not connected")
