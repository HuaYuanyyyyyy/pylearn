from fastapi import APIRouter
from app.model.model_dto import ModelDTO
from app.service.model_service import ModelService

router = APIRouter(prefix="/models", tags=["models"])
service = ModelService()

@router.get("/")
def get_all_models():
    return service.get_all_models()

@router.get("/{model_id}")
def get_model(model_id: int):
    return service.get_model(model_id)

@router.post("/")
def create_model(model: ModelDTO):
    return service.create_model(model)

@router.delete("/{model_id}")
def delete_model(model_id: int):
    service.delete_model(model_id)
    return {"message": f"模型 {model_id} 已删除"}

@router.put("/{model_id}/deploy")
def deploy_model(model_id: int):
    service.deploy_model(model_id)
    return {"message": f"模型 {model_id} 已部署"}