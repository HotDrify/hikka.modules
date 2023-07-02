# ---------------------------------------------------------------------------------
# 🔒 Licensed under the GNU AGPLv3.
# 🚬 Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: freeAI
# Author: HotDrify
# Commands:
# .prompt
# ---------------------------------------------------------------------------------
#          █░█ █▀█ ▀█▀ █▀▄ █▀█ █ █▀▀ █▄█ ░ █░█ █ █▄▀ █▄▀ ▄▀█
#          █▀█ █▄█ ░█░ █▄▀ █▀▄ █ █▀░ ░█░ ▄ █▀█ █ █░█ █░█ █▀█
#          🔒 Licensed under the GNU AGPLv3. | https://www.gnu.org/licenses/agpl-3.0.html
#                                 @HotDrify
# requires: git+https://github.com/HotDrify/freeAI
# scope: hikka_only
# scope: hikka_min 1.2.10

import logging
from freeAI import aichatos
from telethon.tl.types import Message
# type: ignore
from telethon.tl.functions.users import GetFullUserRequest
from .. import loader, utils

class AIMod(loader.Module):
    strings = {
      'name' : 'freeAI',
      '_input_text' : '📌 write yes or no.',
      'wait_text' : '🕒 wait...',
      'args_err' : '❌ you forgot to ask a question.'
    }
    strings_ru = {
      '_input_text' : '📌 напишите только yes или no.',
      'wait_text' : '🕒 ждите...',
      'args_err' : '❌ вы забыли задать вопрос.'
    }
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                'automsg',
                'no',
                lambda: self.strings('_input_text'),
            ),
        )
    async def watcher(self, message):
        reply = await message.get_reply_message()
        if not reply:
            return
        aichat = await aichatos.Running.main(message.text)
        e = await message.reply(self.strings('wait_text'))
        await e.edit(aichat['result'][0]['content'])
    @loader.unrestricted
    async def promptcmd(self, message: Message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(
              message,
              self.strings('args_err')
            )
            return
        await utils.answer(message, self.strings('wait_text').format(args=args))
        aichat = await aichatos.Running.main(args)
        await utils.answer(
          message,
          aichat['result'][0]['content']
        )