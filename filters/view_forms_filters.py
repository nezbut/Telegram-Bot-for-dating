from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from abc import ABC, abstractmethod
from fluentogram import TranslatorRunner
from states import FSMViewForms
from .form_fill_filters import BaseChoiceFilter

class BaseViewFormsFilter(BaseFilter, ABC):

    async def __call__(self, message: Message, i18n: TranslatorRunner, state: FSMContext) -> bool:
        if FSMViewForms.view_forms == await state.get_state():

            return message.text == self.get_trigger_symbol(i18n=i18n)

    @abstractmethod
    def get_trigger_symbol(self, i18n: TranslatorRunner) -> str:
        pass

class LikeFilter(BaseViewFormsFilter):

    def get_trigger_symbol(self, i18n: TranslatorRunner) -> str:
        return i18n.view_forms_btns.like()

class LikeAndCommentFilter(BaseViewFormsFilter):

    def get_trigger_symbol(self, i18n: TranslatorRunner) -> str:
        return i18n.view_forms_btns.like_and_comment()

class DislikeFilter(BaseViewFormsFilter):

    def get_trigger_symbol(self, i18n: TranslatorRunner) -> str:
        return i18n.view_forms_btns.dislike()

class CrossFilter(BaseViewFormsFilter):

    def get_trigger_symbol(self, i18n: TranslatorRunner) -> str:
        return i18n.view_forms_btns.cross()

class CommentFilter(BaseChoiceFilter):
    filter_state = FSMViewForms.writes_comment.state

    def _filter(self, message: Message, state: FSMContext, i18n: TranslatorRunner) -> Any:
        if message.text and message.text.strip() == i18n.cancel_button().strip():
            return {
                "comment": None,
                "video": None
            }

        elif message.text and len(message.text) <= 300:
            return {
                "comment": message.text.strip(),
                "video": None
            }

        elif message.video and message.video.duration <= 15:
            return {
                "comment": None,
                "video": message.video.file_id
            }

    def _get_error_message(self, i18n: TranslatorRunner) -> str:
        return i18n.writing_comment_error()

__all__ = (
    'LikeFilter',
    'LikeAndCommentFilter',
    'DislikeFilter',
    'CrossFilter',
    'CommentFilter'
)
