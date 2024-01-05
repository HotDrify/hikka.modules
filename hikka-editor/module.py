# ---------------------------------------------------------------------------------
#          █░█ █▀█ ▀█▀ █▀▄ █▀█ █ █▀▀ █▄█ ░ █░█ █ █▄▀ █▄▀ ▄▀█
#          █▀█ █▄█ ░█░ █▄▀ █▀▄ █ █▀░ ░█░ ▄ █▀█ █ █░█ █░█ █▀█
#                      🔒 Licensed under the GNU AGPLv3.
#                                 @HotDrify
# requires: git+https://github.com/HotDrify/freeAI
# scope: hikka_only
# scope: hikka_min 1.6.3

from telethon.tl.types import Message

from .. import loader, utils

@loader.tds
class HikkaEditorMod(loader.Module):
    """Hikka strings editor"""
    strings = {
        'name': 'Hikka-Editor',
        'ignore.version': '📦 Если true - отключает проверку версии hikka (при отключении могут быть неполадки.)'
    }
