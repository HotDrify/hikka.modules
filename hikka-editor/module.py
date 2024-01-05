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
        'edited': '✅ <b>Готово!</b>'
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

    @loader.command()
    async def editversioncmd(self, message: Message):
        """📦 Изменяет версию Hikka."""
        args = utils.get_args_raw(message)
        await utils.answer(message, self.strings["editing"])
        version.__version__ = tuple(map(int, args.split(".")))
        await utils.answer(message, self.strings["edited"])

    @loader.command()
    async def edituptimecmd(self, message: Message):
        """📦 Изменяет время запуска. (e: 1y 205d 10:12:35)"""
        args = utils.get_args_raw(message)
        await utils.answer(message, self.strings["editing"])
        
        time_components = args.split(" ")
        date_components = time_components[:-1]
        time_component = time_components[-1]
        duration = datetime.timedelta(*[
            int(x[:-1]) * (365 if x.endswith("y") else 1)
            if x[-1] in ["y", "d"]
            else int(x)
            for x in date_components
        ])

        current_datetime = datetime.datetime.now()
        future_datetime = current_datetime + duration
        time_list = [int(x) for x in time_component.split(":")]
        time = datetime.time(*time_list)
        future_datetime_with_time = datetime.datetime.combine(future_datetime.date(), time)

        timestamp = future_datetime_with_time.timestamp()

        utils.init_ts = timestamp
        
        await utils.answer(message, self.strings["edited"])
        
        
