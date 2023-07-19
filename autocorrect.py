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
# scope: hikka_only
# scope: hikka_min 1.2.10

from .. import loader, utils
import logging

import requests

logger = logging.getLogger(__name__)

@loader.tds
class autoCorrectMod(loader.Module):
    """❤️ автоматическое исправление текста."""
    
    strings = {
      "name": "autoCorrect",
      "status": "📌 включение и выключение автозамены.",
      "lang": "📌 язык",
      "link": "📌 не даст изменить сообщение с ссылкой.",
      "slash": "📌 не даст изменить сообщение с слеш командой (/).",
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
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
        
        if self.config["is_slash"]:
            if "/" in message.text:
                return
        
        if self.config["is_link"]:
            if "https" in message.text or "http" in message.text:
                return
                
        response = requests.get(
          "https://speller.yandex.net/services/spellservice.json/checkText",
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