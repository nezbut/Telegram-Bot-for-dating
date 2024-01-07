from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext

from fluentogram import TranslatorRunner
from keyboards import ReadyInlineKeyboards
from states import FSMMainMenu, FSMForm
from database import MongoDB
from utils import answer_user_form, ViewForms

router = Router()

@router.message(CommandStart(), ~StateFilter(FSMMainMenu.language))
async def start(
    message: Message,
    i18n: TranslatorRunner,
    ready_inline_kb: ReadyInlineKeyboards,
    state: FSMContext,
    db: MongoDB,
    view_forms: ViewForms
):
    await state.clear()

    user_id = message.from_user.id
    user_form = await db.get_user_form(id_user=user_id)

    await view_forms.clear(
        user_id=user_id,
        view_form_id=await view_forms.get_view_form_user(user_id=user_id)
    )

    if user_form:
        await state.set_state(FSMMainMenu.menu)

        return await answer_user_form(
            user_form=user_form,
            tg_obj=message,
            i18n=i18n
        )

    await message.answer(
        text=f"{i18n.start()}\n{i18n.language_choice()}",
        reply_markup=ready_inline_kb.languages(where="start")
    )

    await state.set_state(FSMMainMenu.language)

@router.message(Command("myprofile"))
async def myprofile(message: Message, i18n: TranslatorRunner, state: FSMContext, db: MongoDB, view_forms: ViewForms):
    user_id = message.from_user.id
    form = await db.get_user_form(id_user=user_id)

    await state.clear()
    await view_forms.clear(
        user_id=user_id,
        view_form_id=await view_forms.get_view_form_user(user_id=user_id)
    )

    if not form:
        await message.answer(
            text=f"{i18n.form_not_exist()}\n{i18n.age_choice()}",
            reply_markup=ReplyKeyboardRemove()
        )

        return await state.set_state(FSMForm.age)

    await answer_user_form(
        user_form=form,
        tg_obj=message,
        i18n=i18n
    )

    await state.set_state(FSMMainMenu.menu)

@router.message(Command("help"))
async def help(message: Message, i18n: TranslatorRunner):

    await message.answer(
        text=f"{i18n.commands.help(username=message.from_user.first_name)}"
    )
