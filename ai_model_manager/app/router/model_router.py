from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from app.model.model_dto import ModelDTO
from app.repository.model_repository import ModelRepository
from app.service.model_service import ModelService

router = APIRouter(prefix="/models", tags=["models"])

def get_service(db: AsyncSession = Depends(get_db)) -> ModelService:
    repo = ModelRepository(db)
    return ModelService(repo)

@router.get("/")
async def get_all_models(service: ModelService = Depends(get_service)):
    return await service.get_all_models()

@router.get("/deployed")
async def get_deployed_models(service: ModelService = Depends(get_service)):
    return await service.get_deployed_models()

@router.get("/{model_id}")
async def get_model(model_id: int, service: ModelService = Depends(get_service)):
    try:
        return await service.get_model(model_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/")
async def create_model(model: ModelDTO, service: ModelService = Depends(get_service)):
    return await service.create_model(model)

@router.delete("/{model_id}")
async def delete_model(model_id: int, service: ModelService = Depends(get_service)):
    try:
        await service.delete_model(model_id)
        return {"message": f"模型 {model_id} 已删除"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{model_id}/deploy")
async def deploy_model(model_id: int, service: ModelService = Depends(get_service)):
    try:
        return await service.deploy_model(model_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))