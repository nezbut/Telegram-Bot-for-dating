from aiogram.types import (
    InlineKeyboardButton,
    WebAppInfo,
    LoginUrl,
    SwitchInlineQueryChosenChat,
    CallbackGame
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .base import BaseKeyboardBuilder

class BuilderInlineKeyboards(BaseKeyboardBuilder):

    builder_class = InlineKeyboardBuilder

    def new_kb_buttons(
        self,
        callback_and_text: dict[str, str],
        url: str = None,
        web_app: WebAppInfo = None,
        login_url: LoginUrl = None,
        switch_inline_query: str = None,
        switch_inline_query_current_chat: str = None,
        switch_inline_query_chosen_chat: SwitchInlineQueryChosenChat = None,
        callback_game: CallbackGame = None,
        pay: bool = None,
    ):
        self._new_buttons(
            buttons_call_data_or_text=callback_and_text,
            class_btn=InlineKeyboardButton,
            url=url,
            web_app=web_app,
            login_url=login_url,
            switch_inline_query=switch_inline_query,
            switch_inline_query_current_chat=switch_inline_query_current_chat,
            switch_inline_query_chosen_chat=switch_inline_query_chosen_chat,
            callback_game=callback_game,
            pay=pay
        )

    def new_first_buttons(
        self,
        callback_and_text: dict[str, str],
        url: str = None,
        web_app: WebAppInfo = None,
        login_url: LoginUrl = None,
        switch_inline_query: str = None,
        switch_inline_query_current_chat: str = None,
        switch_inline_query_chosen_chat: SwitchInlineQueryChosenChat = None,
        callback_game: CallbackGame = None,
        pay: bool = None,
    ):
        self._new_buttons(
            buttons_call_data_or_text=callback_and_text,
            new_first_btn=True,
            class_btn=InlineKeyboardButton,
            url=url,
            web_app=web_app,
            login_url=login_url,
            switch_inline_query=switch_inline_query,
            switch_inline_query_current_chat=switch_inline_query_current_chat,
            switch_inline_query_chosen_chat=switch_inline_query_chosen_chat,
            callback_game=callback_game,
            pay=pay
        )

    def new_last_buttons(
        self,
        callback_and_text: dict[str, str],
        url: str = None,
        web_app: WebAppInfo = None,
        login_url: LoginUrl = None,
        switch_inline_query: str = None,
        switch_inline_query_current_chat: str = None,
        switch_inline_query_chosen_chat: SwitchInlineQueryChosenChat = None,
        callback_game: CallbackGame = None,
        pay: bool = None,
    ):
        self._new_buttons(
            buttons_call_data_or_text=callback_and_text,
            new_last_btn=True,
            class_btn=InlineKeyboardButton,
            url=url,
            web_app=web_app,
            login_url=login_url,
            switch_inline_query=switch_inline_query,
            switch_inline_query_current_chat=switch_inline_query_current_chat,
            switch_inline_query_chosen_chat=switch_inline_query_chosen_chat,
            callback_game=callback_game,
            pay=pay
        )

__all__ = (
    'BuilderInlineKeyboards',
)
