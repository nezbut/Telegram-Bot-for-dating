from typing import Any, Awaitable, Callable, Dict
from utils import ViewForms

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class ViewFormsMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
        ) -> Any:

        db = data["db"]
        redis = data["redis"]

        view_forms = ViewForms(database=db, redis=redis)

        data["view_forms"] = view_forms
        return await handler(event, data)

__all__ = (
    'ViewFormsMiddleware',
)
