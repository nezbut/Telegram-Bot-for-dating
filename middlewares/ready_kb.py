from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from typing import Any, Awaitable, Callable, Dict
from keyboards import ReadyInlineKeyboards, ReadyReplyKeyboards

class ReadyKeyboardsMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
        ) -> Any:

        data['ready_inline_kb'] = ReadyInlineKeyboards()
        data['ready_reply_kb'] = ReadyReplyKeyboards()
        
        return await handler(event, data)

__all__ = (
    'ReadyKeyboardsMiddleware',
)
