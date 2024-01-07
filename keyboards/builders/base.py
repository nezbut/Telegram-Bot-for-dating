from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, ButtonType
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

from abc import ABC, abstractmethod

class BaseKeyboardBuilder(ABC):

    builder_class: ReplyKeyboardBuilder | InlineKeyboardBuilder | None = None

    def __init__(
            self,
            width: int = 1,
            last_buttons_width: int = 2,
            first_buttons_width: int = 2,
        ) -> None:

        self.width = width
        self.last_btns_width = last_buttons_width
        self.first_btns_width = first_buttons_width

        self.buttons: list[ButtonType] = []
        self.first_buttons: list[ButtonType] = []
        self.last_buttons: list[ButtonType] = []

    def build_keyboard(
            self,
            width: int | None = None,
            last_buttons_width: int | None = None,
            first_buttons_width: int | None = None,
            **kwargs
        ) -> ReplyKeyboardMarkup | InlineKeyboardMarkup:

        width = width if isinstance(width, int) else self.width
        first_buttons_width = first_buttons_width if isinstance(first_buttons_width, int) else self.first_btns_width
        last_buttons_width = last_buttons_width if isinstance(last_buttons_width, int) else self.last_btns_width

        builder: ReplyKeyboardBuilder | InlineKeyboardBuilder = self.builder_class()

        if not self.buttons:
            return

        if self.first_buttons:
            builder.row(*self.first_buttons, width=first_buttons_width)

        builder.row(*self.buttons, width=width)

        if self.last_buttons:
            builder.row(*self.last_buttons, width=last_buttons_width)

        if hasattr(self, "resize_keyboard"):
            return builder.as_markup(resize_keyboard=self.resize_keyboard, **kwargs)

        return builder.as_markup(**kwargs)

    def _new_buttons(
        self,
        buttons_call_data_or_text: dict[str, str] | list[str],
        new_first_btn=False,
        new_last_btn=False,
        class_btn: ButtonType | None = None,
        **kwargs
    ):

        kb_list: list[ButtonType] = []

        if isinstance(buttons_call_data_or_text, list):

            for btn_text in buttons_call_data_or_text:
                kb_list.append(
                    class_btn(
                        text=btn_text,
                        **kwargs
                    )
                )

        else:

            for btn_callback_data, btn_text in buttons_call_data_or_text.items():
                kb_list.append(
                    class_btn(
                        text=btn_text,
                        callback_data=btn_callback_data,
                        **kwargs
                    )
                )

        if new_first_btn:
            self.first_buttons.extend(kb_list)

        elif new_last_btn:
            self.last_buttons.extend(kb_list)

        else:
            self.buttons.extend(kb_list)

    @abstractmethod
    def new_kb_buttons(self):
        pass

    @abstractmethod
    def new_first_buttons(self):
        pass

    @abstractmethod
    def new_last_buttons(self):
        pass
