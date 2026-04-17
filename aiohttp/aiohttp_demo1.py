import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://httpbin.org/get") as resp:
            data = await resp.json()
            print(data)

asyncio.run(main())