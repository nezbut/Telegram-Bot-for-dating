from aiogram.filters.callback_data import CallbackData

class LanguageChoiceCallbackFactory(CallbackData, prefix="language_choice"):
    language: str
    where: str

class GenderChoiceCallbackFactory(CallbackData, prefix="gender"):
    gender_type: str

class InterestedInGenderCallbackFactory(CallbackData, prefix="interested_in_gender"):
    interested_in_gender: str

class ConfirmationCallbackFactory(CallbackData, prefix="confirmation"):
    answer: str

__all__ = (
    'LanguageChoiceCallbackFactory',
    'GenderChoiceCallbackFactory',
    'InterestedInGenderCallbackFactory',
    'ConfirmationCallbackFactory'
)
