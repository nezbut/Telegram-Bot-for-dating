from aiogram import Router
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query()
async def other_callbacks(callback: CallbackQuery):
    await callback.answer()