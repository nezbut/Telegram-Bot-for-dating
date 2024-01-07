from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.storage.redis import Redis

from typing import Any, Awaitable, Callable, Dict
from fluentogram import TranslatorHub

from database import MongoDB

class TranslatorRunnerMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
        ) -> Any:

        db: MongoDB = data['db']
        user_id: int = data['event_from_user'].id
        name_user: str = data['event_from_user'].first_name
        username: str | None = data['event_from_user'].username
        hub: TranslatorHub = data.get("t_hub")
        red: Redis = data['redis']

        lang_code: bytes | None = await red.get(f"language:{user_id}")

        if lang_code:
            lang_code = lang_code.decode().lower().strip()

        else:
            lang_code = await db.get_language_user(id_user=user_id)

            if not lang_code:
                lang_code = data['event_from_user'].language_code

                await db.insert_user(
                    id_user=user_id,
                    name_user=name_user,
                    lang_code=lang_code,
                    username=username
                )

            await red.setex(
                name=f"language:{user_id}",
                time=43200,
                value=lang_code
            )

        data['i18n'] = hub.get_translator_by_locale(locale=lang_code)
        return await handler(event, data)

__all__ = (
    'TranslatorRunnerMiddleware',
)
