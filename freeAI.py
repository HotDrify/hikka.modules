# ---------------------------------------------------------------------------------
# 🔒 Licensed under the GNU AGPLv3.
# 🚬 Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: freeAI
# Author: HotDrify
# Commands:
# .prompt
# .banChat
# .unbanChannel
# ---------------------------------------------------------------------------------
#          █░█ █▀█ ▀█▀ █▀▄ █▀█ █ █▀▀ █▄█ ░ █░█ █ █▄▀ █▄▀ ▄▀█
#          █▀█ █▄█ ░█░ █▄▀ █▀▄ █ █▀░ ░█░ ▄ █▀█ █ █░█ █░█ █▀█
#                      🔒 Licensed under the GNU AGPLv3.
#                                 @HotDrify
# requires: git+https://github.com/HotDrify/freeAI
# scope: hikka_only
# scope: hikka_min 1.2.10

import logging
from freeAI import minigpt

from telethon.tl.types import Message
from telethon.tl.functions.users import GetFullUserRequest
# type: ignore

from .. import loader, utils

class AIMod(loader.Module):
    strings = {
      'name' : 'freeAI',
      '_input_text' : '📌 acts like an answering machine.',
      'wait_text' : '🕒 wait...',
      'args_err' : '❌ you forgot to ask a question.',
      'chat_err' : '❌ failed to perform this action. check if this chat is in the list.',
      'banned_text' : '🖕 chat is blocked.'
    }
    strings_ru = {
      '_input_text' : '📌 действует по типу "автоответчик".',
      'wait_text' : '🕒 ждите...',
      'args_err' : '❌ вы забыли задать вопрос.',
      'chat_err' : '❌ не удалось выполнить это действие. проверьте, есть ли этот чат в списке.',
      'banned_text' : '🖕 успешно.'
    }
    def __init__(self):
        _db = self._db
        self._channels = self.pointer('blockedChats', [])
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                'automsg',
                False,
                lambda: self.strings('_input_text'),
                validator = loader.validators.Boolean(),
            ),
        )
    async def watcher(self, message):
        reply = await message.get_reply_message()
        if self.config['automsg'] == True:
            if not reply:
                return
            if reply.from_id == self._tg_id:
                if reply.peer_id.channel_id in self._channels:
                    return
                e = await message.reply(self.strings('wait_text'))
                mini = await minigpt.Running.main(message.text)
                await e.edit(mini['result'][0]['content'])
    @loader.unrestricted
    async def banChatcmd(self):
        chat = await event.get_chat()
        if chat.id in self._channels:
            await utils.answer(
              message,
              self.strings('channel_err')
            )
            return
        await utils.answer(
          message,
          self.strings('banned_text')
        )
        self._channels.append(chat.id)
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
        mini = await minigpt.Running.main(args)
        await utils.answer(
          message,
          mini['result'][0]['content']
        )