from datetime import datetime
import json
import re
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import AsyncOpenAI
from app.router.get_weather import fetch_weather
from app.config.database import AsyncSessionLocal
from app.repository.model_repository import ModelRepository
from app.service.model_service import ModelService

router = APIRouter(prefix="/chat", tags=["chat"])

client = AsyncOpenAI(
    api_key="sk-167fff19c26f401fad8277f93a21ee35",
    base_url="https://api.deepseek.com"
)

all_messages = [{"role": "system", "content":"""你是一个AI模型管理系统的助手，
                可以查询模型列表、查询天气、获取当前时间等等问题。
                回答要简洁，使用中文。
                示例：
                    用户：系统里有几个模型？
                    助手：系统中共有 X 个模型",分别为"a","b"
                在回答问题之前，请先分析用户的意图，判断需要调用哪个工具，然后再给出答案。    
                """}]

# 所有回答必须以 JSON 格式返回，格式为：{"answer": "回答内容", "tool_used": "使用的工具名或null"}

#定义查询全部模型工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_all_models",        # 函数名，AI 调用时会用这个名字
            "description": "获取系统中所有AI模型的列表",  # 告诉 AI 这个工具干什么用，描述要清晰
            "parameters": {
                "type": "object",
                "properties": {},            # 这个工具不需要参数，所以是空的
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前系统时间，返回 YYYY-MM-DD HH:MM:SS 格式",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取指定城市当前天气，例如温度、天气描述、湿度",
            "parameters": {
                "type": "object",
                "properties": {
                    "city":{
                        "type":"string",
                        "description":"城市名，例如beijing，shanghai，shenzhen"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

class ChatRequest(BaseModel):
    message: str

@router.post("/func")
async def chat(request: ChatRequest):
    all_messages.append({"role": "user", "content": request.message})
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages = all_messages,
        tools=tools,        # 把工具定义传进去
        tool_choice="auto",
    )
    # response_format={"type": "json_object"}
    
    # 有值走函数调用，没有值走普通回答
    if response.choices[0].message.tool_calls:
        # 返回tool_call是否有值
        tool_call  = response.choices[0].message.tool_calls[0]
        #调用AI tools
        result :str = ""
        function_name = tool_call.function.name  # 取出函数名
        if function_name == "get_all_models":
            # 调用你自己的 service 获取模型列表
            # 把结果转成字符串
            async with AsyncSessionLocal() as db:
                repo = ModelRepository(db)
                service = ModelService(repo)
                models = await service.get_all_models()
                result = str([m.name for m in models])
        elif function_name == "get_current_time":
            result = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif function_name == "get_current_weather":
            args = json.loads(tool_call.function.arguments or "{}")
            city = args.get("city", "").strip()
            if not city:
                result = "缺少 city 参数，请提供城市名"
            else:
                result = await fetch_weather(city)
        # 结果取出来
        all_messages.append(response.choices[0].message)
        all_messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })  
        async def generate():
            # 再发一次请求，让 AI 根据结果回答
            final_response = await client.chat.completions.create(
                model="deepseek-chat",
                messages=all_messages,
                stream=True
            )
        # print(final_response.choices[0].message.content)
            chunks :str = ""  
            async for chunk in final_response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
            all_messages.append({"role":"assistant","content":chunks})        
        return StreamingResponse(generate(), media_type="text/plain")
    else:
        async def generate():
            stream_resp = await client.chat.completions.create(
            model="deepseek-chat",
            messages=all_messages,
            stream=True,
            )
            chunks :str = ""
            async for chunk in stream_resp:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
            all_messages.append({"role": "assistant", "content": chunks})        
        return StreamingResponse(generate(), media_type="text/plain")

    # chunks: str = ""
    # async for chunk in response:
    #     if chunk.choices[0].delta.content != None:
    #         print(chunk.choices[0].delta.content,end="", flush=True)
    #         chunks = chunks + chunk.choices[0].delta.content
    # #结束追加
    print()
    print(f"总共的--->{all_messages}")
    # return all_messages
         