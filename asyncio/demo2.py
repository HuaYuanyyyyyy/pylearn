import asyncio
from functools import wraps

def retry_async(max_retries=3):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for i in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"重试 {i+1}/{max_retries}: {e}")
                    if i == max_retries - 1:
                        print("❌ 重试耗尽，彻底失败")
                        raise Exception(f"重试{max_retries}次后仍失败: {last_exception}") from None  # from None 可以简化堆栈
            raise Exception("重试耗尽")
        return wrapper
    return decorator

attempt_count = 0

@retry_async(max_retries=3)
async def call_llm(prompt):
    global attempt_count
    attempt_count += 1
    await asyncio.sleep(0.5)
    
    if attempt_count <= 3:
        raise Exception(f"第 {attempt_count} 次调用失败")
    
    return f"LLM 回答: {prompt} (第 {attempt_count} 次成功)"

async def main():
    try:
        result = await call_llm("讲个笑话")
        print(result)
    except Exception as e:
        print(f"程序捕获: {e}")

asyncio.run(main())