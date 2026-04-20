import os
import aiohttp


async def fetch_weather(city: str) -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "天气服务未配置 OPENWEATHER_API_KEY"

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",   # 摄氏度
        "lang": "zh_cn"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, timeout=10) as resp:
            if resp.status != 200:
                text = await resp.text()
                return f"查询天气失败，status={resp.status}, detail={text}"
            data = await resp.json()

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    desc = data["weather"][0]["description"]
    return f"{city} 当前天气：{desc}，温度 {temp}°C，湿度 {humidity}%"