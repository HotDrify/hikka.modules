# ---------------------------------------------------------------------------------
# 🔒 Licensed under the GNU AGPLv3.
# 🚬 Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: freeAI
# Author: HotDrify
# Commands:
# .prompt
# .banChat
# .unbanChat
# .addword
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
      'banWord_text' : '❌ Your request contains forbidden text',
      'automsg_text' : '📌 acts like an answering machine.',
      'wait_text' : '🕒 wait...',
      'args_err' : '❌ you forgot to enter arguments',
      'chat_err' : '❌ failed to perform this action. check if this chat is in the list.',
      'banned_text' : '🖕 chat is blocked.'
    }
    strings_ru = {
      'automsg_text' : '📌 действует по типу "автоответчик".',
      'banWord_text' : '❌ в твоём запросе есть запрещённый текст',
      'wait_text' : '🕒 ждите...',
      'args_err' : '❌ вы забыли ввести аргументы.',
      'chat_err' : '❌ не удалось выполнить это действие. проверьте, есть ли этот чат в списке.',
      'banned_text' : '🖕 успешно.'
    }
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                'waitText',
                True,
                lambda: self.strings('wait._text'),
                validator = loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                'automsg',
                False,
                lambda: self.strings('automsg_text'),
                validator = loader.validators.Boolean(),
            ),
        )
        
    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        if not self.get('banWords', False):
            self.set('banWords', [])
        if not self.get('banChats', False):
            self.set('banChats', [])
            
    async def watcher(self, message):
        reply = await message.get_reply_message()
        if self.config['automsg']:
            if self.get('banWords') in message.text:
                await message.reply(self.strings['banWord_text'])
            if message.is_private:
                if self.config['waitText']:
                    repl = await message.reply(self.strings['wait_text'])
                    mini = await minigpt.Running.main(message.text)
                    await repl.edit(mini['result'][0]['content'])
                if not self.config['waitText']:
                    mini = await minigpt.Running.main(message.text)
                    await message.reply(mini['result'][0]['content'])
            if not reply:
                return
            if reply.from_id == self._tg_id:
                if reply.peer_id.channel_id in self.get('banChats'):
                    return
                if self.config['waitText']:
                    repl = await message.reply(self.strings['wait_text'])
                    mini = await minigpt.Running.main(message.text)
                    await repl.edit(mini['result'][0]['content'])
                if not self.config['waitText']:
                    mini = await minigpt.Running.main(message.text)
                    await message.reply(mini['result'][0]['content'])
    
    @loader.unrestricted
    async def addwordcmd(self, message: Message):
        args = utils.get_args_raw(message)
        if not args:
            await message.answer(
              message,
              self.strings('args_err')
            )
            return
        await utils.answer(
          message,
          self.strings('banned_text')
        )
        list = self.get('banWords')
        list.append(message.text)
        self.set('banWords', list)
    @loader.unrestricted
    async def unbanChatcmd(self, message: Message):
        """
        снять кляп жизни.
        """
        chat = await message.get_chat()
        if chat.id not in self.get('banChats'):
            await utils.answer(
              message,
              self.strings('chat_err')
            )
            return
        await utils.answer(
          message,
          self.strings('banned_text')
        )
        list = self.get('banChats')
        list.remove(chat.id)
        self.set('banChats', list)
    @loader.unrestricted
    async def banChatcmd(self, message: Message):
        """
        бот не будет реагировать на сообщения данного чата.
        """
        chat = await message.get_chat()
        if chat.id in self.get('banChats'):
            await utils.answer(
              message,
              self.strings('chat_err')
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
        """
        задать вопрос.
        """
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