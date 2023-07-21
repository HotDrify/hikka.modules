# ---------------------------------------------------------------------------------
# 🔒 Licensed under the GNU AGPLv3.
# 🚬 Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: autoCorrect
# Author: HotDrify
# ---------------------------------------------------------------------------------
#          █░█ █▀█ ▀█▀ █▀▄ █▀█ █ █▀▀ █▄█ ░ █░█ █ █▄▀ █▄▀ ▄▀█
#          █▀█ █▄█ ░█░ █▄▀ █▀▄ █ █▀░ ░█░ ▄ █▀█ █ █░█ █░█ █▀█
#                      🔒 Licensed under the GNU AGPLv3.
#                                 @HotDrify
from .. import loader, utils
import logging

import requests
import json

logger = logging.getLogger(__name__)

@loader.tds
class autoCorrectMod(loader.Module):
    """❤️ автоматическое исправление текста."""
    
    strings = {
      "name": "autoCorrect",
      "status": "📌 включение и выключение автозамены.",
      "lang": "📌 язык",
      "link": "📌 если включен: не даст изменить сообщение с ссылкой.",
      "slash": "📌 если включен: не даст изменить сообщение с слеш командой (/).",
      "api_base": "🛠️ (эта функция только для создателя, не знаешь, не трогай!) позволяет изменить API_BASE.",
      "ping": "📌 если включен: не даст изменить сообщение с упоминанием (@)"
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
              "is_ping",
              True,
              lambda: self.strings["ping"],
            ),
            loader.ConfigValue(
              "api_base",
              'https://speller.yandex.net/services/spellservice.json/checkText',
              lambda: self.strings["api_base"],
              validator = loader.validators.Link(),
            ),
            loader.ConfigValue(
              "is_slash",
              True,
              lambda: self.strings["slash"],
              validator = loader.validators.Boolean(),
            ),
            loader.ConfigValue(
              "is_link",
              True,
              lambda: self.strings["link"],
              validator = loader.validators.Boolean(),
            ),
            loader.ConfigValue(
              "lang",
              "ru",
              lambda: self.strings["lang"],
              validator = loader.validators.Choice(["ru", "en"]),
          ),
          loader.ConfigValue(
              "status_work",
              True,
              lambda: self.strings["status"],
              validator = loader.validators.Boolean(),
          ),
        )

    @loader.tag("only_messages", "no_commands", "out")
    async def watcher(self, message):
        if not self.config["status_work"]:
            return
        
        if self.config["is_ping"]:
            if "@" in message.text:
                return
        
        if self.config["is_slash"]:
            if "/" in message.text:
                return
        
        if self.config["is_link"]:
            if "https" in message.text or "http" in message.text:
                return
                
        response = requests.get(
          self.config["api_base"],
          params = {
            'text': message.text,
            'lang': self.config['lang'],
            'options': 512
          }
        )
        
        data = response.json()
        ctext = message.text
        
        for mistake in data:
            ctext = ctext[:mistake['pos']] + mistake['s'][0] + ctext[mistake['pos']+mistake['len']:]
        
        if message.text != ctext:
            await message.edit(ctext)