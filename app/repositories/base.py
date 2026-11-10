from collections.abc import Mapping
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

_FORBIDDEN = (";", "--", "/*", "*/")


class BaseRepository:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession], *, max_rows: int) -> None:
        self._session_factory = session_factory
        self._max_rows = max_rows

    async def fetch_all(self, statement: str, params: Mapping[str, Any]) -> list[dict[str, Any]]:
        _assert_single_statement(statement)
        if ":limit" not in statement:
            raise ValueError("query must include a bound :limit")
        bound = dict(params)
        requested = int(bound.get("limit", self._max_rows))
        bound["limit"] = min(max(requested, 1), self._max_rows)
        async with self._session_factory() as session:
            result = await session.execute(text(statement), bound)
            return [dict(row) for row in result.mappings().all()]


def _assert_single_statement(statement: str) -> None:
    if any(token in statement for token in _FORBIDDEN):
        raise ValueError("query must be a single bound statement")
