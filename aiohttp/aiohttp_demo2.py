import asyncio
import aiohttp

async def download_large_file(url, filename):
    """流式下载大文件，避免内存爆炸"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            # 获取文件大小
            total_size = int(resp.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filename, 'wb') as f:
                # 每块 8KB 写入
                async for chunk in resp.content.iter_chunked(8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        progress = downloaded / total_size * 100
                        print(f"\r下载进度: {progress:.1f}%", end='')
            
            print(f"\n✅ 下载完成: {filename}")

async def main():
    # 下载一个测试文件
    url = "https://httpbin.org/bytes/102400"  # 100KB 测试文件
    await download_large_file(url, "test.bin")

asyncio.run(main())