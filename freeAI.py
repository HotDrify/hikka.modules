# ---------------------------------------------------------------------------------
# № Licensed under the GNU AGPLv3.
# т яИ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
#---------------------------------------------------------------------------------
#          лАллплплплпмлплллпплмлАлАлллмплмпмпл
#          лпллмлАлАлмплпмллпААлАмлплллАллАллпл
#           Licensed under the GNU AGPLv3. | https://www.gnu.org/licenses/agpl-3.0.html
#                                 @HotDrify
# requires: git+https://github.com/HotDrify/freeAI
# scope: hikka_only
# scope: hikka_min 1.2.10

import logging
from freeAI import aichatos

from .. import loader, utils

class AIMod(loader.Module):
    strings = {
      'wait_text' : ' wait...',
      'args_err' : ' you forgot to ask a question.'
    }
    strings_ru = {
      'wait_text' : ' ждите...',
      'args_err' : ' вы забыли задать вопрос.'
    }
    
    @loader.unrestricted
    async def promptcmd(self, message: Message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(
              message,
              self.strings("args_err")
            )
            return
        await utils.answer(message, self.strings("wait_text").format(args=args))
        aichat = await aichatos.Running.main("hi")
        await utils.answer(message, aichat)