from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from typing import Any
from states import FSMViewForms
from fluentogram import TranslatorRunner
from .form_fill_filters import BaseChoiceFilter

class ViewLikesLikeFilter(BaseChoiceFilter):
    filter_state = FSMViewForms.view_like.state

    def _filter(self, message: Message, state: FSMContext, i18n: TranslatorRunner) -> Any:
        return message.text and message.text.strip() == i18n.view_forms_btns.like().strip()

class ViewLikesDislikeFilter(BaseChoiceFilter):
    filter_state = FSMViewForms.view_like.state

    def _filter(self, message: Message, state: FSMContext, i18n: TranslatorRunner) -> Any:
        return message.text and message.text.strip() == i18n.view_forms_btns.dislike().strip()

class ViewLikesContinueFilter(BaseChoiceFilter):
    filter_state = FSMViewForms.view_like.state

    def _filter(self, message: Message, state: FSMContext, i18n: TranslatorRunner) -> Any:
        return message.text and message.text.strip() == i18n.contin().strip()

__all__ = (
    'ViewLikesLikeFilter',
    'ViewLikesDislikeFilter',
    'ViewLikesContinueFilter'
)
