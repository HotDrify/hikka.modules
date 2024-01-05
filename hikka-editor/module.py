# ---------------------------------------------------------------------------------
#          █░█ █▀█ ▀█▀ █▀▄ █▀█ █ █▀▀ █▄█ ░ █░█ █ █▄▀ █▄▀ ▄▀█
#          █▀█ █▄█ ░█░ █▄▀ █▀▄ █ █▀░ ░█░ ▄ █▀█ █ █░█ █░█ █▀█
#                      🔒 Licensed under the GNU AGPLv3.
#                                 @HotDrify
# requires: git+https://github.com/HotDrify/freeAI
# scope: hikka_only
# scope: hikka_min 1.6.3

from telethon.tl.types import Message
from .. import loader, utils, version
import datetime

@loader.tds
class HikkaEditorMod(loader.Module):
    """Hikka strings editor"""
    strings = {
        'name': 'Hikka-Editor',
        'editing': '⏳ <b>Редактирую...</b>',
        'edited': '✅ <b>Готово!</b>',
        'notfound': '<b>❌ Не найдено!</b>'
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                'ignore.version',
                False,
                '📦 Если true - отключает проверку версии hikka (при отключении могут быть неполадки.)',
                validator=loader.validators.Boolean(),
            )
        )

    async def client_ready(self, client, db):
        self.db = db

    @loader.command()
    async def editversion(self, message: Message):
        """📦 Изменяет версию Hikka."""
        args = utils.get_args_raw(message)
        await utils.answer(message, self.strings["editing"])
        version.__version__ = tuple(map(int, args.split(".")))
        await utils.answer(message, self.strings["edited"])

    @loader.command()
    async def editplatform(self, message: Message):
        """📦 Изменяет платформу на котророй стоит Hikka."""
        args = utils.get_args_raw(message)
        await utils.answer(message, self.strings["editing"])

        def platform():
            return args
        
        utils.get_named_platform = platform
        await utils.answer(message, self.strings["edited"])

    @loader.command()
    async def setbperiod(self, message: Message):
        """📦 Изменяет период бекапа (в минутах.)."""
        args = utils.get_args_raw(message)
        await utils.answer(message, self.strings["editing"])
        self.db.set("HikkaBackupMod", "period", int(args) * 60)
        await utils.answer(message, self.strings["edited"])

