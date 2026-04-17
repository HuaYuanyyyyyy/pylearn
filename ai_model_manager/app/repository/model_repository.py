from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.model.model_entity import ModelEntity

class ModelRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> ModelEntity | None:
        result = await self.db.execute(select(ModelEntity).where(ModelEntity.id == id))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ModelEntity]:
        result = await self.db.execute(select(ModelEntity))
        return list(result.scalars().all())

    async def get_deployed(self) -> list[ModelEntity]:
        result = await self.db.execute(select(ModelEntity).where(ModelEntity.is_deployed == True))
        return list(result.scalars().all())

    async def create(self, entity: ModelEntity) -> ModelEntity:
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def update(self, entity: ModelEntity) -> ModelEntity:
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def delete(self, entity: ModelEntity) -> None:
        await self.db.delete(entity)
        await self.db.commit()