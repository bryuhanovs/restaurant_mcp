from datetime import date

from app.repositories.write_offs_repository import WriteOffsRepository


class WriteOffsService:
    def __init__(self, repository: WriteOffsRepository) -> None:
        self._repository = repository

    async def write_offs(
        self,
        restaurant_id: str,
        date_from: date,
        date_to: date,
    ) -> list[dict[str, object]]:
        return await self._repository.write_offs(restaurant_id, date_from, date_to)
