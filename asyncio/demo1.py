import asyncio
import time
from unittest import result

#让 Python 写并发代码像写同步代码一样简单，通过单线程+事件循环实现高并发 I/O 操作。

# 定义协程
async def say_hello():
    print("Hello")
    await asyncio.sleep(1)  # 模拟 I/O 操作
    print("World")

# 调用协程（方式一：直接创建任务）
async def main():
    await say_hello() 

# asyncio.run(main())
#进阶

#并发执行任务
async def print_A():
    print("a 开始")
    loop = asyncio.get_running_loop()  # 获取当前运行的事件循环
    print(f"事件循环: {loop}")
    await asyncio.sleep(2)
    print("a 结束")
    return "结果a"

async def print_B():
    print("b 开始")
    loop = asyncio.get_running_loop()  # 获取当前运行的事件循环
    print(f"事件循环: {loop}")
    await asyncio.sleep(3)
    print("b 结束")
    return "结果b"

async def main_print():
    result = await asyncio.gather(print_A(),print_B())
    print(result)

# asyncio.run(main_print())


""" 
什么是事件循环？
本质：不停运转的调度器，维护两个队列（就绪队列 + 等待队列），循环执行以下步骤：

text
1. 从就绪队列取出一个任务执行
2. 任务遇到 await 时暂停，把任务放回等待队列
3. 等待的 I/O 完成后，把任务移回就绪队列
4. 重复步骤 1 
"""""

async def demo():
    print("运行中...")
    return "完成"

# asyncio.run(demo())   


#创建任务/等待超时

async def slow_operation():
    await asyncio.sleep(3)
    return "完成"

async def main_create():
    # 方式一：create_task（Python 3.7+ 推荐）
    task1 = asyncio.create_task(slow_operation())
    
    # 方式二：ensure_future（更通用）
    task2 = asyncio.ensure_future(slow_operation())
    
    # 等待所有任务
    # results = await asyncio.gather(task1, task2)
    try:
        result = await asyncio.wait_for(slow_operation(),timeout=2)
    except:
        print("等待超时")
        

# asyncio.run(main_create())    


async def fetch(url):
    await asyncio.sleep(1)  # 模拟网络请求
    return f"数据从 {url}"
    
async def serial():
    start = time.time()
    r1 = await fetch("url1")
    r2 = await fetch("url2")
    r3 = await fetch("url3")
    print(f"串行耗时: {time.time() - start:.1f}s")

# 并发执行：总耗时 1 秒
async def concurrent():
    start = time.time()
    results = await asyncio.gather(
        fetch("url1"),
        fetch("url2"),
        fetch("url3")
    )
    print(f"并发耗时: {time.time() - start:.1f}s")

asyncio.run(serial())
asyncio.run(concurrent())



