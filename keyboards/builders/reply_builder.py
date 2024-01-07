from aiogram.types import (
    KeyboardButton,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUser,
    KeyboardButtonPollType,
    WebAppInfo
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from .base import BaseKeyboardBuilder

class BuilderReplyKeyboards(BaseKeyboardBuilder):

    builder_class = ReplyKeyboardBuilder

    def __init__(
            self,
            width: int = 1,
            last_buttons_width: int = 2,
            first_buttons_width: int = 2,
            resize_keyboard: bool = True
        ) -> None:

        self.resize_keyboard = resize_keyboard
        super().__init__(width, last_buttons_width, first_buttons_width)

    def new_kb_buttons(
        self,
        buttons_text: list[str],
        request_user: KeyboardButtonRequestUser | None = None,
        request_chat: KeyboardButtonRequestChat | None = None,
        request_contact: bool | None = None,
        request_location: bool | None = None,
        request_poll: KeyboardButtonPollType | None = None,
        web_app: WebAppInfo | None = None,
    ):
        self._new_buttons(
            buttons_call_data_or_text=buttons_text,
            class_btn=KeyboardButton,
            request_user=request_user,
            request_chat=request_chat,
            request_contact=request_contact,
            request_location=request_location,
            request_poll=request_poll,
            web_app=web_app
        )

    def new_first_buttons(
        self,
        buttons_text: list[str],
        request_user: KeyboardButtonRequestUser | None = None,
        request_chat: KeyboardButtonRequestChat | None = None,
        request_contact: bool | None = None,
        request_location: bool | None = None,
        request_poll: KeyboardButtonPollType | None = None,
        web_app: WebAppInfo | None = None,
    ):
        self._new_buttons(
            buttons_call_data_or_text=buttons_text,
            new_first_btn=True,
            class_btn=KeyboardButton,
            request_user=request_user,
            request_chat=request_chat,
            request_contact=request_contact,
            request_location=request_location,
            request_poll=request_poll,
            web_app=web_app
        )

    def new_last_buttons(
        self,
        buttons_text: list[str],
        request_user: KeyboardButtonRequestUser | None = None,
        request_chat: KeyboardButtonRequestChat | None = None,
        request_contact: bool | None = None,
        request_location: bool | None = None,
        request_poll: KeyboardButtonPollType | None = None,
        web_app: WebAppInfo | None = None,
    ):
        self._new_buttons(
            buttons_call_data_or_text=buttons_text,
            new_last_btn=True,
            class_btn=KeyboardButton,
            request_user=request_user,
            request_chat=request_chat,
            request_contact=request_contact,
            request_location=request_location,
            request_poll=request_poll,
            web_app=web_app
        )

__all__ = (
    'BuilderReplyKeyboards',
)
