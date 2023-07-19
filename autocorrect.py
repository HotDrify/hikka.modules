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
import json

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
      "api_base": "🛠️ (эта функция только для создателя, не знаешь, не трогай!) позволяет изменить API_BASE.",
      "api_params": "🛠️ (эта функция только для создателя, не знаешь, не трогай!) %text% - text, %lang% - lang. позволяет изменить API_PARAMS."
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
              "api_params",
              '{"text": "%text%", "lang": "%lang%", "options": 512}',
              lambda: self.strings["api_params"],
              validator = loader.validators.String(),
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
        
        if self.config["is_slash"]:
            if "/" in message.text:
                return
        
        if self.config["is_link"]:
            if "https" in message.text or "http" in message.text:
                return
        
        json_data = json.loads(self.config["api_params"].replace("%text%", message.text).replace("%lang%", self.config["lang"]))
        
        response = requests.get(
          self.config["api_base"],
          params = json_data
        )
        
        data = response.json()
        ctext = message.text
        
        for mistake in data:
            ctext = ctext[:mistake['pos']] + mistake['s'][0] + ctext[mistake['pos']+mistake['len']:]
        
        if message.text != ctext:
            await message.edit(ctext)