from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Mapped tables are added after the restaurant schema is connected."""
