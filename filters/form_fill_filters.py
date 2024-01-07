from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import FSMForm
from fluentogram import TranslatorRunner
from abc import ABC, abstractmethod

class BaseChoiceFilter(BaseFilter, ABC):
    filter_state: str = None

    async def __call__(self, message: Message, state: FSMContext, i18n: TranslatorRunner) -> Any:
        if self.filter_state == await state.get_state():

            result_filter = self._filter(message=message, state=state, i18n=i18n)

            if result_filter:
                return result_filter

            error_msg = self._get_error_message(i18n=i18n)
            if error_msg and isinstance(error_msg, str):
                await message.answer(
                    text=error_msg
                )

    @abstractmethod
    def _filter(self, message: Message, state: FSMContext, i18n: TranslatorRunner) -> Any:
        pass

    def _get_error_message(self, i18n: TranslatorRunner) -> str:
        pass

class AgeChoiceFilter(BaseChoiceFilter):
    filter_state = FSMForm.age.state

    def _filter(self, message: Message, state: FSMContext, i18n: TranslatorRunner) -> Any:
        if message.text and message.text.isdigit():

            age = int(message.text)

            if 14 <= age <= 80:
                return {"age": age}

    def _get_error_message(self, i18n: TranslatorRunner) -> str:
        return i18n.error_age_choice()

class CityChoiceFilter(BaseChoiceFilter):
    filter_state = FSMForm.city.state

    def _filter(self, message: Message, state: FSMContext, i18n: TranslatorRunner) -> Any:
        if message.text and len(message.text) >= 2:
            return {
                "city": message.text.strip()[:65]
            }

    def _get_error_message(self, i18n: TranslatorRunner) -> str:
        return i18n.error_city_choice()

class NameChoiceFilter(BaseChoiceFilter):
    filter_state = FSMForm.name.state

    def _filter(self, message: Message, state: FSMContext, i18n: TranslatorRunner) -> Any:
        if message.text:
            return {
                "name": message.text.strip()[:30]
            }

    def _get_error_message(self, i18n: TranslatorRunner) -> str:
        return i18n.error_name_choice()

class AboutMeChoiceFilter(BaseChoiceFilter):
    filter_state = FSMForm.about_me.state

    def _filter(self, message: Message, state: FSMContext, i18n: TranslatorRunner) -> Any:
        if message.text:
            text = "not_change_button" if message.text.strip() == i18n.not_change_button().strip() else message.text.strip()

            return {
                "about_me": text[:820]
            }

    def _get_error_message(self, i18n: TranslatorRunner) -> str:
        return i18n.error_about_me_choice()

class PhotoOrVideoChoiceFilter(BaseChoiceFilter):
    filter_state = FSMForm.photo_or_video.state

    def _filter(self, message: Message, state: FSMContext, i18n: TranslatorRunner) -> Any:
        if message.photo or (message.video and message.video.duration <= 15):

            photo = message.photo
            video = message.video

            return {
                "photo_id": photo[-1].file_id if photo else photo,
                "video_id": video.file_id if video else video,
                "no_change_button": False
            }

        elif message.text and message.text.strip() == i18n.not_change_button().strip():

            return {
                "photo_id": None,
                "video_id": None,
                "no_change_button": True
            }

    def _get_error_message(self, i18n: TranslatorRunner) -> str:
        return i18n.error_photo_or_video_choice()

__all__ = (
    'AgeChoiceFilter',
    'CityChoiceFilter',
    'NameChoiceFilter',
    'AboutMeChoiceFilter',
    'PhotoOrVideoChoiceFilter'
)
