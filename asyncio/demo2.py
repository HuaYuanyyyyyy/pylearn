import asyncio
from functools import wraps

def retry_async(max_retries=4):
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

@retry_async(max_retries=4)
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


""" 
时间 0.00秒：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[main] 调用 call_llm("讲个笑话")
  ↓
[wrapper] 进入第1次循环 (i=0)
  ↓
[wrapper] 执行 return await func(*args, **kwargs)
  ↓ (遇到 await，让出控制权)
  
[call_llm] 开始执行
  ↓
[call_llm] attempt_count = 1
  ↓
[call_llm] 执行 await asyncio.sleep(0.5)
  ↓ (遇到 await，再次让出控制权)
  
[事件循环] 检查：还有其他任务吗？
  → 没有！只有一个任务
  → 进入等待状态（不占 CPU）
  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

时间 0.50秒：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[定时器触发] asyncio.sleep(0.5) 完成
  ↓
[事件循环] 唤醒 call_llm 任务
  ↓
[call_llm] 从 await 处继续执行
  ↓
[call_llm] 检查: attempt_count=1 <=3 → True
  ↓
[call_llm] raise Exception("第 1 次调用失败")
  ↓
[异常] 传递回 wrapper
  ↓
[wrapper] 捕获异常，打印 "重试 1/4: 第 1 次调用失败"
  ↓
[wrapper] i=0, 不是最后一次 (max_retries=4)
  ↓
[wrapper] 继续第2次循环 (i=1)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

时间 0.50秒（立即）：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[wrapper] 第2次循环: return await func(*args, **kwargs)
  ↓ (遇到 await，让出控制权)
  
[call_llm] 再次执行
  ↓
[call_llm] attempt_count = 2
  ↓
[call_llm] 执行 await asyncio.sleep(0.5)
  ↓ (遇到 await，让出控制权)
  
[事件循环] 又进入等待状态

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

时间 1.00秒：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[定时器触发] 第2次 sleep 完成
  ↓
[call_llm] 被唤醒，检查 attempt_count=2 <=3 → True
  ↓
[call_llm] raise Exception("第 2 次调用失败")
  ↓
[wrapper] 捕获，打印 "重试 2/4: 第 2 次调用失败"
  ↓
[wrapper] 第3次循环 (i=2)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

时间 1.00秒（立即）：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[wrapper] 第3次循环
[call_llm] attempt_count = 3
[call_llm] await asyncio.sleep(0.5)
[事件循环] 等待...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

时间 1.50秒：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[定时器触发] 第3次 sleep 完成
[call_llm] 检查: attempt_count=3 <=3 → True
[call_llm] raise Exception("第 3 次调用失败")
[wrapper] 打印 "重试 3/4: 第 3 次调用失败"
[wrapper] 第4次循环 (i=3)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

时间 1.50秒（立即）：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[wrapper] 第4次循环
[call_llm] attempt_count = 4
[call_llm] await asyncio.sleep(0.5)
[事件循环] 等待...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

时间 2.00秒：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[定时器触发] 第4次 sleep 完成
[call_llm] 检查: attempt_count=4 <=3 → False
[call_llm] 返回 f"LLM 回答: 讲个笑话 (第 4 次成功)"
[wrapper] 收到结果，return
[main] 打印结果




 """