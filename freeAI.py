# ---------------------------------------------------------------------------------
# 🔒 Licensed under the GNU AGPLv3.
# 🚬 Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: freeAI
# Author: HotDrify
# Commands:
# .prompt
# .banChat
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
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                'automsg',
                False,
                lambda: self.strings('_input_text'),
                validator = loader.validators.Boolean(),
            ),
        )
    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        if not self.get('banChats', False):
            self.set('banChats', [])
    async def watcher(self, message):
        reply = await message.get_reply_message()
        if self.config['automsg'] == True:
            if not reply:
                return
            if reply.from_id == self._tg_id:
                if reply.peer_id.channel_id in self.get('banChats'):
                    return
                e = await message.reply(self.strings('wait_text'))
                mini = await minigpt.Running.main(message.text)
                await e.edit(mini['result'][0]['content'])
    @loader.unrestricted
    async def banChatcmd(self, message: Message):
        chat = await message.get_chat()
        if chat.id in self.get('banChats'):
            await utils.answer(
              message,
              self.strings('channel_err')
            )
            return
        await utils.answer(
          message,
          self.strings('banned_text')
        )
        list = self.get('banChats')
        list.append(chat.id)
        self.set('banChats', list)
        
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