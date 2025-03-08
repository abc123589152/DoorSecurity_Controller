import httpx
import asyncio

async def send_gpio_output_request():
    url = "http://172.16.1.100:5020/eventaction/message"
    payload = {"outputPort": ["15", "16"]}  # 需要開啟的 GPIO port

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        print(response.json())

# 在 async 環境下執行
asyncio.run(send_gpio_output_request())
