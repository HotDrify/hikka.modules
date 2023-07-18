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
      "status": "📌 включение и выключение автозамены."
    }
    
    async def __init__(self):
        self.config = loader.ModuleConfig(
          loader.ConfigValue(
            "lang",
            "ru",
            validator=loader.validators.MultiChoice(["ru", "en"]),
          ),
          loader.ConfigValue(
            "statusWork",
            True,
            lambda: self.strings["status"],
            validator = loader.validators.Boolean(),
          ),
        )

    @loader.tag("only_messages", "no_commands", "out")
    async def watcher(self, message):
        if not self.config["statusWork"]:
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
        await message.edit(ctext)