from aiogram import Router
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import Redis

from fluentogram import TranslatorRunner, TranslatorHub
from database import MongoDB
from keyboards import ReadyInlineKeyboards, ReadyReplyKeyboards
from states import FSMForm, FSMMainMenu
from keyboards.callback_factorys import (
    LanguageChoiceCallbackFactory,
    GenderChoiceCallbackFactory,
    InterestedInGenderCallbackFactory,
    ConfirmationCallbackFactory
)
from utils import answer_user_form
import asyncio

router = Router()

@router.callback_query(LanguageChoiceCallbackFactory.filter(), StateFilter(FSMMainMenu.language))
async def language_choice_callback(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: LanguageChoiceCallbackFactory,
    db: MongoDB,
    redis: Redis,
    t_hub: TranslatorHub
):
    language = callback_data.language.lower().strip()
    user_id = callback.from_user.id
    i18n = t_hub.get_translator_by_locale(locale=language)

    await asyncio.gather(
        db.update_language_user(id_user=user_id, new_lang_code=language),
        redis.setex(name=f"language:{user_id}", time=43200, value=language)
    )

    await callback.message.delete()

    if callback_data.where != "start":
        form = await db.get_user_form(id_user=callback.from_user.id)

        await state.set_state(FSMMainMenu.menu)

        return await answer_user_form(
            user_form=form,
            tg_obj=callback,
            i18n=i18n
        )

    await callback.message.answer(
        text=i18n.age_choice(),
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(FSMForm.age)

@router.callback_query(GenderChoiceCallbackFactory.filter(), StateFilter(FSMForm.gender))
async def gender_choice_callback(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: GenderChoiceCallbackFactory,
    i18n: TranslatorRunner,
    ready_inline_kb: ReadyInlineKeyboards
):
    user_gender = callback_data.gender_type.lower().strip()

    await state.update_data(gender=user_gender)

    await callback.message.delete()

    await callback.message.answer(
        text=i18n.choice_interested_gender(),
        reply_markup=ready_inline_kb.interested_in_gender(
            boys=i18n.boys(),
            girls=i18n.girls(),
            no_matter=i18n.no_matter()
        )
    )

    await state.set_state(FSMForm.interested_in_gender)

@router.callback_query(InterestedInGenderCallbackFactory.filter(), StateFilter(FSMForm.interested_in_gender))
async def interested_in_gender_choice_callback(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: InterestedInGenderCallbackFactory,
    i18n: TranslatorRunner,
    ready_reply_kb: ReadyReplyKeyboards,
    db: MongoDB
):

    form = await db.get_user_form(id_user=callback.from_user.id)
    user_interested_in_gender = callback_data.interested_in_gender.lower().strip()

    await state.update_data(interested_in_gender=user_interested_in_gender)

    await callback.message.delete()

    await callback.message.answer(
        text=i18n.city_choice(),
        reply_markup=ready_reply_kb.one_button(text=form["city"]) if form else ReplyKeyboardRemove()
    )

    await state.set_state(FSMForm.city)

@router.callback_query(ConfirmationCallbackFactory.filter(), StateFilter(FSMForm.confirmation))
async def confirmation_choice_callback(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ConfirmationCallbackFactory,
    i18n: TranslatorRunner,
    ready_reply_kb: ReadyReplyKeyboards,
    db: MongoDB
):
    user_answer = callback_data.answer.strip()
    form = await db.get_user_form(id_user=callback.from_user.id)

    if user_answer != "yes":

        await callback.message.delete()

        await state.clear()
        await state.set_state(FSMForm.age)

        return await callback.message.answer(
            text=i18n.age_choice(),
            reply_markup=ready_reply_kb.one_button(text=form["age"]) if form else ReplyKeyboardRemove()
        )

    data_in_redis = await state.get_data()
    data_in_redis["id_user"] = callback.from_user.id

    if not form:

        await db.insert_user_form(**data_in_redis)

        data_in_redis.update(
            {
                "form_status": "included",
                "instagram_url": "not"
            }
        )

    else:
        await db.update_user_form(**data_in_redis)

        photo_id_or_video_id = "photo_id" if data_in_redis.get("photo_id") else "video_id"

        append_data = {
            photo_id_or_video_id: form[photo_id_or_video_id] if data_in_redis[photo_id_or_video_id] == "not_change_button" else data_in_redis[photo_id_or_video_id],
            "about_me": form["about_me"] if data_in_redis["about_me"] == "not_change_button" else data_in_redis["about_me"],
            "form_status": form["form_status"],
            "instagram_url": form["instagram_url"]
        }

        data_in_redis.update(append_data)

    await state.clear()

    await callback.message.delete()

    await answer_user_form(
        user_form=data_in_redis,
        tg_obj=callback,
        i18n=i18n
    )

    await state.set_state(FSMMainMenu.menu)
