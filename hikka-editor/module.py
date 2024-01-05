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
import re

@loader.tds
class HikkaEditorMod(loader.Module):
    """Hikka strings editor"""
    strings = {
        'name': 'Hikka-Editor'
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
    async def modinfocmd(self, message: Message):
        """📦 Изменяет версию Hikka."""
        args = utils.get_args_raw(message)
        version.__version__ = tuple(map(int, args.split(".")))
        await utils.answer(message, "готово!")
        
    
