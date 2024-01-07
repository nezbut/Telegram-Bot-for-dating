from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from fluentogram import TranslatorRunner
from database import MongoDB
from keyboards import ReadyInlineKeyboards, ReadyReplyKeyboards
from states import FSMForm
from filters import (
    AgeChoiceFilter,
    CityChoiceFilter,
    NameChoiceFilter,
    AboutMeChoiceFilter,
    PhotoOrVideoChoiceFilter
)

router = Router()

@router.message(AgeChoiceFilter())
async def age_choice(
    message: Message,
    age: int,
    state: FSMContext,
    i18n: TranslatorRunner,
    ready_inline_kb: ReadyInlineKeyboards
):

    await state.update_data(age=age)

    await message.answer(
        text=i18n.good(),
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        text=i18n.gender_choice(),
        reply_markup=ready_inline_kb.gender_choice(
            boy=i18n.boy(),
            girl=i18n.girl()
        )
    )

    await state.set_state(FSMForm.gender)

@router.message(CityChoiceFilter())
async def city_choice(
    message: Message,
    city: str,
    state: FSMContext,
    i18n: TranslatorRunner,
    ready_reply_kb: ReadyReplyKeyboards,
    db: MongoDB
):

    await state.update_data(city=city)

    form = await db.get_user_form(id_user=message.from_user.id)

    await message.answer(
        text=i18n.name_choice(),
        reply_markup=ready_reply_kb.one_or_two_buttons(
            one=message.from_user.first_name,
            two=form["name"] if form else None
        )
    )

    await state.set_state(FSMForm.name)

@router.message(NameChoiceFilter())
async def name_choice(
    message: Message,
    name: str,
    state: FSMContext,
    i18n: TranslatorRunner,
    ready_reply_kb: ReadyReplyKeyboards,
    db: MongoDB
):

    await state.update_data(name=name)

    form = await db.get_user_form(id_user=message.from_user.id)

    await message.answer(
        text=i18n.about_me_choice(),
        reply_markup=ready_reply_kb.one_or_two_buttons(
            one=i18n.skip_button(),
            two=i18n.not_change_button() if form and form["about_me"] != "not" else None
        )
    )

    await state.set_state(FSMForm.about_me)

@router.message(AboutMeChoiceFilter())
async def about_me_choice(
    message: Message,
    about_me: str,
    state: FSMContext,
    i18n: TranslatorRunner,
    ready_reply_kb: ReadyReplyKeyboards,
    db: MongoDB
):
    if about_me.strip() == i18n.skip_button().strip():
        await state.update_data(about_me="not")

    else:
        await state.update_data(about_me=about_me)

    form_exists = await db.exists_user_form(id_user=message.from_user.id)

    await message.answer(
        text=i18n.photo_or_video_choice(),
        reply_markup=ready_reply_kb.one_button(text=i18n.not_change_button()) if form_exists else ReplyKeyboardRemove()
    )

    await state.set_state(FSMForm.photo_or_video)

@router.message(PhotoOrVideoChoiceFilter())
async def photo_or_video_choice(
    message: Message,
    photo_id: str | None,
    video_id: str | None,
    no_change_button: bool,
    state: FSMContext,
    i18n: TranslatorRunner,
    ready_inline_kb: ReadyInlineKeyboards,
    db: MongoDB
):
    if no_change_button:

        form = await db.get_user_form(id_user=message.from_user.id)

        photo = form.get("photo_id")

        if photo:
            await state.update_data(photo_id="not_change_button")

        else:
            await state.update_data(video_id="not_change_button")

    else:
        if photo_id:
            await state.update_data(photo_id=photo_id)

        else:
            await state.update_data(video_id=video_id)

    await message.answer(
        text=i18n.good(),
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        text=i18n.confirmation_choice(),
        reply_markup=ready_inline_kb.confirmation(
            yes=i18n.yes_button(),
            change=i18n.confirmation_change_button()
        )
    )

    await state.set_state(FSMForm.confirmation)
