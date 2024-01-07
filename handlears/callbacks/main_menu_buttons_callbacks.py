from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.answers import (
    MainMenuCallbackFactory,
    answer_main_menu,
    answer_user_form,
    answer_like_form
)

from fluentogram import TranslatorRunner
from states import FSMMainMenu, FSMForm, FSMViewForms
from keyboards import ReadyInlineKeyboards, ReadyReplyKeyboards
from database import MongoDB
from utils import ViewForms

router = Router()

@router.callback_query(MainMenuCallbackFactory.filter(F.button == "view_forms"), FSMMainMenu.menu)
async def view_forms_button(
    callback: CallbackQuery,
    view_forms: ViewForms,
    i18n: TranslatorRunner,
    ready_reply_kb: ReadyReplyKeyboards,
    state: FSMContext,
    db: MongoDB
):
    user_id = callback.from_user.id
    user_form = await db.get_user_form(id_user=user_id)

    if user_form["form_status"] == "off":
        return await callback.answer(text=i18n.form_off_and_view_forms())

    first_form = await view_forms.get_next_form_for_user(user_id=user_id)

    if first_form:

        await callback.message.delete()
        await callback.message.answer(
            text=i18n.first_view_form(),
            reply_markup=ready_reply_kb.buttons_view_forms(i18n=i18n)
        )

        await answer_user_form(
            user_form=first_form,
            tg_obj=callback,
            i18n=i18n,
            answer_first_msg=False,
            answer_menu=False
        )

        return await state.set_state(FSMViewForms.view_forms)

    await callback.answer(text=i18n.no_forms_found())

@router.callback_query(MainMenuCallbackFactory.filter(F.button == "change_form"), FSMMainMenu.menu)
async def change_form_button(callback: CallbackQuery,
    state: FSMContext,
    i18n: TranslatorRunner,
    db: MongoDB,
    ready_reply_kb: ReadyReplyKeyboards
):

    form = await db.get_user_form(id_user=callback.from_user.id)

    await callback.message.delete()

    await state.clear()
    await state.set_state(FSMForm.age)

    await callback.message.answer(
        text=i18n.age_choice(),
        reply_markup=ready_reply_kb.one_button(
            text=str(form["age"])
        )
    )

@router.callback_query(MainMenuCallbackFactory.filter(F.button == "change_photo_or_video"), FSMMainMenu.menu)
async def change_photo_or_video_button(callback: CallbackQuery,
    state: FSMContext,
    ready_reply_kb: ReadyReplyKeyboards,
    i18n: TranslatorRunner
):

    await callback.message.delete()

    await callback.message.answer(
        text=i18n.photo_or_video_choice(),
        reply_markup=ready_reply_kb.one_button(
            text=i18n.not_change_button()
        )
    )

    await state.set_state(FSMMainMenu.photo_or_video_change)

@router.callback_query(MainMenuCallbackFactory.filter(F.button == "change_about_me"), FSMMainMenu.menu)
async def change_about_me_button(callback: CallbackQuery,
    state: FSMContext,
    ready_reply_kb: ReadyReplyKeyboards,
    i18n: TranslatorRunner
):

    await callback.message.delete()

    await callback.message.answer(
        text=i18n.about_me_choice(),
        reply_markup=ready_reply_kb.one_or_two_buttons(
            one=i18n.not_change_button(),
            two=i18n.remove_about_me()
        )
    )

    await state.set_state(FSMMainMenu.about_me_change)

@router.callback_query(MainMenuCallbackFactory.filter(F.button == "language"), FSMMainMenu.menu)
async def language_button(callback: CallbackQuery,
    state: FSMContext,
    i18n: TranslatorRunner,
    ready_inline_kb: ReadyInlineKeyboards
):

    await callback.message.edit_text(
        text=i18n.language_choice(),
        reply_markup=ready_inline_kb.languages(where="main_menu")
    )

    await state.set_state(FSMMainMenu.language)

@router.callback_query(MainMenuCallbackFactory.filter(F.button == "insta"), FSMMainMenu.menu)
async def insta_button(callback: CallbackQuery,
    state: FSMContext,
    i18n: TranslatorRunner,
    ready_reply_kb: ReadyReplyKeyboards
):

    await callback.message.delete()

    await callback.message.answer(
        text=i18n.insta(),
        reply_markup=ready_reply_kb.one_button(text=i18n.cancel_button())
    )

    await state.set_state(FSMMainMenu.insta)

@router.callback_query(MainMenuCallbackFactory.filter(F.button == "un_insta"), FSMMainMenu.menu)
async def un_insta_button(callback: CallbackQuery,
    i18n: TranslatorRunner,
    db: MongoDB
):

    await db.update_instagram_url_user(id_user=callback.from_user.id, url="not")
    form = await db.get_user_form(id_user=callback.from_user.id)
    form_status = form.get("form_status")

    await answer_main_menu(
        tg_obj=callback,
        i18n=i18n,
        instagram=False,
        form_status=form_status,
        edit=True
    )

    await callback.answer(text=i18n.done_unlinked_insta())

@router.callback_query(MainMenuCallbackFactory.filter(F.button.in_(["form_off", "form_included"])), FSMMainMenu.menu)
async def form_included_or_form_off_button(callback: CallbackQuery,
    i18n: TranslatorRunner,
    db: MongoDB,
    callback_data: MainMenuCallbackFactory
):
    user_id = callback.from_user.id
    new_form_status = "off" if callback_data.button.strip() == "form_off" else "included"

    await db.update_form_status_user(id_user=user_id, new_status=new_form_status)

    form = await db.get_user_form(id_user=user_id)
    instagram = False if form.get("instagram_url") == "not" else True
    form_status = form.get("form_status")

    await answer_main_menu(
        tg_obj=callback,
        i18n=i18n,
        instagram=instagram,
        form_status=form_status,
        edit=True
    )

    await callback.answer(text=i18n.form_successfully_disabled() if new_form_status == "off" else i18n.form_successfully_included())

@router.callback_query(MainMenuCallbackFactory.filter(F.button == "view_like"), FSMMainMenu.menu)
async def view_like_button(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    state: FSMContext,
    view_forms: ViewForms,
    ready_reply_kb: ReadyReplyKeyboards
):

    next_like_form = await view_forms.get_next_form_like_user(user_id=callback.from_user.id)

    if not next_like_form:
        return await callback.answer(text=i18n.no_likes())

    await callback.message.delete()

    await answer_like_form(
        form=next_like_form,
        tg_obj=callback,
        i18n=i18n,
        reply_markup=ready_reply_kb.buttons_view_likes(i18n=i18n)
    )

    await state.set_state(FSMViewForms.view_like)
