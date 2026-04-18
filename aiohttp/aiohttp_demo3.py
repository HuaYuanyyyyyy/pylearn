import asyncio
import aiohttp


async def aiohttp_demo():
    """ 发送数据 """
    data = {
        'name': 'job',
        'age' : 18,
        'hobbies': ["game","sport"]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://httpbin.org/post', json=data) as resp:
            result = await resp.json()
            print(f"发送数据{data}")
            print(f"返回数据{result}")

asyncio.run(aiohttp_demo())



""" aiohttp 是异步 HTTP 客户端，配合 asyncio 可以实现万级并发，比同步 requests 快几十倍，特别适合爬虫、调用 LLM API、批量请求等 I/O 密集型场景。

现在你可以：

用 aiohttp 替代 requests 做批量请求

结合你之前学的重试装饰器

用信号量控制并发数

用流式处理大文件/SSE

试试修改你之前的 call_llm 函数，用 aiohttp 发送真实的 HTTP 请求 """
