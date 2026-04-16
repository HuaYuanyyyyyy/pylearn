from functools import wraps
from typing import Any, Callable, Generator, Literal
from pydantic import BaseModel, Field


# log_operation
def log_operation(operation_name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def inner(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"[LOG] 开始执行: {operation_name}")
            try:
                result = func(*args, **kwargs)
                print(f"[LOG] 执行成功: {operation_name}")
                return result
            except Exception as e:
                print(f"[LOG] 执行失败: {operation_name}, 错误: {e}")
                raise

        return wrapper

    return inner




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
modelAI1 = ModelDTO(
    name = "2",
    type = "CV",
    version = "1.0.3",
    parameterSize = 1.00,
    isDeployed = True)    
# print(modelAI)
# print(modelAI.model_dump())

class ModelService:
    def __init__(self) -> None:
        self.db: dict[int, ModelDTO] = {}
        self.id_counter: int = 1

    @log_operation("获取模型")    
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
    def yield_model(self) -> Generator[ModelDTO,None,None]:
        for model in self.db.values():
            yield model
        

service = ModelService()
m1 = service.create_model(modelAI)
m2 = service.create_model(modelAI1)
# print(service.get_all_models())
# service.deploy_model(1)
# print(service.get_deployed_models())
# service.delete_model(1)
# print(service.get_all_models())

# for model in service.yield_model():
#     print(model)

gen = service.yield_model()
print(next(gen))
print(next(gen))

print(service.get_model(1))

#