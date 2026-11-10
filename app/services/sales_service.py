from datetime import date

from app.repositories.sales_repository import SalesRepository


class SalesService:
    def __init__(self, repository: SalesRepository) -> None:
        self._repository = repository

    async def restaurant_sales(
        self,
        restaurant_id: str,
        date_from: date,
        date_to: date,
    ) -> list[dict[str, object]]:
        return await self._repository.restaurant_sales(restaurant_id, date_from, date_to)
