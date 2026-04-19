import re
from fastapi import APIRouter
from pydantic import BaseModel
from openai import AsyncOpenAI

router = APIRouter(prefix="/chat", tags=["chat"])

client = AsyncOpenAI(
    api_key="sk-167fff19c26f401fad8277f93a21ee35",
    base_url="https://api.deepseek.com"
)

all_messages = [{"role": "system", "content":"你是一个AI智能助手"}]

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat(request: ChatRequest):
    all_messages.append({"role": "user", "content": request.message})
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages = all_messages,
        stream=True
    )
    chunks: str = ""
    async for chunk in response:
        if chunk.choices[0].delta.content != None:
            print(chunk.choices[0].delta.content,end="", flush=True)
            chunks = chunks + chunk.choices[0].delta.content
    #结束追加            
    all_messages.append({"role":"assistant","content":chunks})
    print(all_messages)   



"""  
最大的问题是重启就丢了。
all_messages 是存在内存里的，服务器一重启，所有对话历史全没了。
还有几个问题：
多用户冲突
现在所有用户共用同一个 all_messages，A 用户和 B 用户的对话会混在一起，A 能看到 B 说过什么。
历史无限增长
对话越来越长，messages 列表越来越大，每次请求都把全部历史发给 API，token 消耗越来越多，最终超出模型的上下文长度限制。
无法多实例部署
W5 要用 Docker 部署，如果起了两个实例，两个实例的内存是独立的，同一个用户的请求可能打到不同实例，历史对话就对不上了。
""" 
#解决方法

""" 
生产环境怎么解决：

用 Redis 存对话历史，key 是用户 ID 或者 session ID
设置最大轮数，比如只保留最近 10 轮
重要对话持久化到 MySQL
 """