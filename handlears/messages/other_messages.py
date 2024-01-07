from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from fluentogram import TranslatorRunner
from states import FSMMainMenu

router = Router()

@router.message(StateFilter(FSMMainMenu.menu, default_state))
async def other_callbacks(message: Message, i18n: TranslatorRunner):
    await message.answer(text=i18n.sorry_do_not_understand())
