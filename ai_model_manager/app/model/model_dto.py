from typing import Literal
from pydantic import BaseModel, Field


class ModelDTO(BaseModel):
    name: str = Field(...,min_length = 1,max_length = 100,description='模型名称')
    type: Literal["LLM","CV","ASR"] = Field(...,description='模型类型')
    version: str = Field(...,pattern= r"^\d+\.\d+\.\d+$",description= '版本号')
    parameterSize: float = Field(...,ge = 0,description='参数量')
    isDeployed: bool = Field(default=False,description="是否部署")