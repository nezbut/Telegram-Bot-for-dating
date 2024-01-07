from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from language import LANGUAGES
from fluentogram import TranslatorRunner

from .builders import BuilderInlineKeyboards, BuilderReplyKeyboards
from .callback_factorys import (
    LanguageChoiceCallbackFactory,
    GenderChoiceCallbackFactory,
    InterestedInGenderCallbackFactory,
    ConfirmationCallbackFactory
)

class ReadyInlineKeyboards:

    @staticmethod
    def one_button(callback_data: CallbackData | str, text: str, **kwargs) -> InlineKeyboardMarkup:
        builder = BuilderInlineKeyboards()

        builder.new_kb_buttons(
            callback_and_text={
                callback_data.pack() if isinstance(callback_data, CallbackData) else callback_data: text
            },
            **kwargs
        )

        return builder.build_keyboard()

    @staticmethod
    def languages(where: str) -> InlineKeyboardMarkup:
        builder = BuilderInlineKeyboards(width=3)

        builder.new_kb_buttons(
            callback_and_text={
                LanguageChoiceCallbackFactory(language=lang_tag[0], where=where).pack(): lang  for lang, lang_tag in LANGUAGES.items()
            }
        )

        return builder.build_keyboard()

    @staticmethod
    def confirmation(yes: str, change: str) -> InlineKeyboardMarkup:
        builder = BuilderInlineKeyboards()

        builder.new_kb_buttons(
            callback_and_text={
                ConfirmationCallbackFactory(answer="yes").pack(): yes,
                ConfirmationCallbackFactory(answer="change").pack(): change
            }
        )

        return builder.build_keyboard()

    @staticmethod
    def gender_choice(boy: str, girl: str) -> InlineKeyboardMarkup:
        builder = BuilderInlineKeyboards(width=2)

        builder.new_kb_buttons(
            callback_and_text={
                GenderChoiceCallbackFactory(gender_type="boy").pack(): boy,
                GenderChoiceCallbackFactory(gender_type="girl").pack(): girl,
            }
        )

        return builder.build_keyboard()

    @staticmethod
    def interested_in_gender(boys: str, girls: str, no_matter: str) -> InlineKeyboardMarkup:
        builder = BuilderInlineKeyboards(width=2)

        builder.new_kb_buttons(
            callback_and_text={
                InterestedInGenderCallbackFactory(interested_in_gender="boys").pack(): boys,
                InterestedInGenderCallbackFactory(interested_in_gender="girls").pack(): girls
            }
        )

        builder.new_last_buttons(
            callback_and_text={
                InterestedInGenderCallbackFactory(interested_in_gender="no_matter").pack(): no_matter,
            }
        )

        return builder.build_keyboard()

class ReadyReplyKeyboards:

    @staticmethod
    def one_button(text: str, **kwargs) -> ReplyKeyboardMarkup:
        builder = BuilderReplyKeyboards()

        builder.new_kb_buttons(
            buttons_text=[text],
            **kwargs
        )
        return builder.build_keyboard()

    @staticmethod
    def one_or_two_buttons(one: str, two: str | None) -> ReplyKeyboardMarkup:
        builder = BuilderReplyKeyboards()

        builder.new_kb_buttons(
            buttons_text=[one]
        )

        if two:

            builder.new_last_buttons(
                buttons_text=[two]
            )

        return builder.build_keyboard()

    @staticmethod
    def buttons_view_forms(i18n: TranslatorRunner) -> ReplyKeyboardMarkup:
        builder = BuilderReplyKeyboards(width=4)

        builder.new_kb_buttons(
            buttons_text=[
                i18n.view_forms_btns.like(),
                i18n.view_forms_btns.like_and_comment(),
                i18n.view_forms_btns.dislike(),
                i18n.view_forms_btns.cross()
            ]
        )

        return builder.build_keyboard()

    @staticmethod
    def buttons_view_likes(i18n: TranslatorRunner) -> ReplyKeyboardMarkup:
        builder = BuilderReplyKeyboards(width=2)

        builder.new_kb_buttons(
            buttons_text=[
                i18n.view_forms_btns.like(),
                i18n.view_forms_btns.dislike(),
            ]
        )

        return builder.build_keyboard()

__all__ = (
    'ReadyInlineKeyboards',
    'ReadyReplyKeyboards'
)
