from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.config import Settings


@dataclass
class AppContext:
    session_factory: async_sessionmaker[AsyncSession]
    settings: Settings
