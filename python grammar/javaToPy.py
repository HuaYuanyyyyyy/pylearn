from re import M
from typing import Literal
from pydantic import BaseModel, Field

class ModelDTO(BaseModel):
    name: str = Field(...,min_length = 1,max_length = 100,description='模型名称')
    type: Literal["LLM","CV","ASR"] = Field(...,description='模型类型')
    version: str = Field(...,pattern= r"^\d+\.\d+\.\d+$",description= '版本号')
    parameterSize: float = Field(...,ge = 0,description='参数量')
    isDeployed: bool = Field(default=False,description="是否部署")

modelAI = ModelDTO(
    name = "1",
    type = "LLM",
    version = "1.0.0",
    parameterSize = 1.00,
    isDeployed = True)
print(modelAI)
print(modelAI.model_dump())

class ModelService:
    def __init__(self) -> None:
        self.db: dict[int, ModelDTO] = {}
        self.id_counter: int = 1

    def get_model(self, id: int) -> ModelDTO:
        model = self.db.get(id)
        if model is None:
            raise ValueError(f"模型 {id} 不存在")
        return model

    def get_all_models(self) -> list[ModelDTO]:
        return list(self.db.values())

    def get_deployed_models(self) -> list[ModelDTO]:
        # 用列表推导写，一行搞定
        return [model for model in self.db.values() if model.isDeployed]

    def create_model(self, model: ModelDTO) -> ModelDTO:
        # 自己补全
        self.db[self.id_counter] = model
        self.id_counter += 1
        return model;

    def deploy_model(self, id: int) -> None:
        # 自己补全
        model = self.db.get(id)
        if model is None:
            raise ValueError(f"模型 {id} 不存在")
        else:
            self.db[id]  = model.model_copy(update={"type": 'CV'})
        return


    def delete_model(self, id: int) -> None:
        # 自己补全
        model = self.db.get(id)
        if model is None:
            raise ValueError(f"模型 {id} 不存在")
        del self.db[id]
        return
        

service = ModelService()
m1 = service.create_model(modelAI)
print(service.get_all_models())
service.deploy_model(1)
print(service.get_deployed_models())
service.delete_model(1)
print(service.get_all_models())
