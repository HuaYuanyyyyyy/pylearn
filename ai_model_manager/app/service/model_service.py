from app.model.model_dto import ModelDTO
from app.model.model_entity import ModelEntity
from app.repository.model_repository import ModelRepository

class ModelService:
    def __init__(self, repo: ModelRepository):
        self.repo = repo

    async def get_model(self, id: int) -> ModelEntity:
        model = await self.repo.get_by_id(id)
        if model is None:
            raise ValueError(f"模型 {id} 不存在")
        return model

    async def get_all_models(self) -> list[ModelEntity]:
        return await self.repo.get_all()

    async def get_deployed_models(self) -> list[ModelEntity]:
        return await self.repo.get_deployed()

    async def create_model(self, dto: ModelDTO) -> ModelEntity:
        entity = ModelEntity(
            name=dto.name,
            type=dto.type,
            version=dto.version,
            parameter_size=dto.parameterSize,
            is_deployed=dto.isDeployed,
        )
        return await self.repo.create(entity)

    async def deploy_model(self, id: int) -> ModelEntity:
        model = await self.get_model(id)
        model.is_deployed = True
        return await self.repo.update(model)

    async def delete_model(self, id: int) -> None:
        model = await self.get_model(id)
        await self.repo.delete(model)