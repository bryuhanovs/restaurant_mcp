from app.repositories.inventory_repository import InventoryRepository


class InventoryService:
    def __init__(self, repository: InventoryRepository) -> None:
        self._repository = repository

    async def stock(self, restaurant_id: str) -> list[dict[str, object]]:
        return await self._repository.stock(restaurant_id)
