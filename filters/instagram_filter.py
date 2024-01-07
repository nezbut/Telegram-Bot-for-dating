from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from typing import Any

from fluentogram import TranslatorRunner
from states import FSMMainMenu
from .form_fill_filters import BaseChoiceFilter

class InstagramUrlFilter(BaseChoiceFilter):
    filter_state = FSMMainMenu.insta.state

    def _filter(self, message: Message, state: FSMContext, i18n: TranslatorRunner) -> Any:
        if message.text:

            if message.text.lower().strip() == i18n.cancel_button().lower().strip():

                return {
                    "instagram_url": None
                }

            if insta_url := self._filter_instagram_url(text=message.text):

                return {
                    "instagram_url": insta_url
                }

    def _get_error_message(self, i18n: TranslatorRunner) -> str:
        return f"{i18n.error_insta()}\n{i18n.error_insta2()}"

    @staticmethod
    def _filter_instagram_url(text: str) -> str | bool:
        instagram_url = "https://www.instagram.com/"

        if text.startswith(instagram_url):
            text = text[len(instagram_url):]

            if text.endswith("/"):
                text = text[:-1]

        if len(text) > 100:
            return False

        for symbol in text:
            if not (symbol.isdigit() or symbol.isalpha() or symbol in (".", "_")):
                return False

        return f"{instagram_url}{text}/"

__all__ = (
    'InstagramUrlFilter',
)
