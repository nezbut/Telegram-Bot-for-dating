from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import Redis

from filters import (
    LikeFilter,
    LikeAndCommentFilter,
    DislikeFilter,
    CrossFilter,
    CommentFilter
)

from utils import (
    ViewForms,
    answer_user_form,
    exit_from_views_forms
)

from states import FSMMainMenu, FSMViewForms
from database import MongoDB
from fluentogram import TranslatorRunner, TranslatorHub
from keyboards import ReadyReplyKeyboards

router = Router()

@router.message(LikeFilter())
async def like_handlear(
    message: Message,
    view_forms: ViewForms,
    t_hub: TranslatorHub,
    i18n: TranslatorRunner,
    db: MongoDB,
    state: FSMContext
):
    user_id = message.from_user.id
    view_form_id = await view_forms.get_view_form_user(user_id=user_id)
    locale = await db.get_language_user(id_user=view_form_id)
    i18n_view_form = t_hub.get_translator_by_locale(locale=locale)

    await view_forms.add_to_exceptions(user_id, view_form_id)
    await view_forms.add_to_likes_user(user_id=view_form_id, new_like_user_id=user_id)

    await message.bot.send_message(
        chat_id=view_form_id,
        text=f"{i18n_view_form.view_forms_send_likes()}\n{i18n_view_form.view_forms_send_likes2()}\n/myprofile",
    )

    form = await view_forms.get_next_form_for_user(user_id=user_id)

    if not form:
        form = await db.get_user_form(id_user=user_id)

        await message.answer(text=i18n.no_forms_found())

        await exit_from_views_forms(
            user_form=form,
            tg_obj=message,
            i18n=i18n,
            view_forms=view_forms
        )

        return await state.set_state(FSMMainMenu.menu)

    await answer_user_form(
        user_form=form,
        tg_obj=message,
        i18n=i18n,
        answer_first_msg=False,
        answer_menu=False
    )

@router.message(LikeAndCommentFilter())
async def like_and_comment_handlear(
    message: Message,
    state: FSMContext,
    ready_reply_kb: ReadyReplyKeyboards,
    i18n: TranslatorRunner
):

    await message.answer(
        text=i18n.writing_comment(),
        reply_markup=ready_reply_kb.one_button(i18n.cancel_button())
    )

    await state.set_state(FSMViewForms.writes_comment)

@router.message(DislikeFilter())
async def dislike_handlear(
    message: Message,
    view_forms: ViewForms,
    i18n: TranslatorRunner,
    db: MongoDB,
    state: FSMContext
):
    user_id = message.from_user.id

    view_form_id = await view_forms.get_view_form_user(user_id=user_id)
    await view_forms.add_to_exceptions(user_id, view_form_id)

    form = await view_forms.get_next_form_for_user(user_id=user_id)

    if not form:
        form = await db.get_user_form(id_user=user_id)

        await message.answer(text=i18n.no_forms_found())

        await exit_from_views_forms(
            user_form=form,
            tg_obj=message,
            i18n=i18n,
            view_forms=view_forms
        )

        return await state.set_state(FSMMainMenu.menu)

    await answer_user_form(
        user_form=form,
        tg_obj=message,
        i18n=i18n,
        answer_first_msg=False,
        answer_menu=False
    )

@router.message(CrossFilter())
async def cross_handlear(
    message: Message,
    view_forms: ViewForms,
    state: FSMContext,
    db: MongoDB,
    i18n: TranslatorRunner
):
    user_id = message.from_user.id
    form = await db.get_user_form(id_user=user_id)

    await exit_from_views_forms(
        user_form=form,
        tg_obj=message,
        i18n=i18n,
        view_forms=view_forms
    )

    await state.set_state(FSMMainMenu.menu)

@router.message(CommentFilter())
async def comment_handlear(
    message: Message,
    comment: str | None,
    video: str | None,
    view_forms: ViewForms,
    state: FSMContext,
    ready_reply_kb: ReadyReplyKeyboards,
    i18n: TranslatorRunner,
    t_hub: TranslatorHub,
    db: MongoDB
):
    user_id = message.from_user.id
    view_form_id = await view_forms.get_view_form_user(user_id=user_id)

    if not comment and not video:
        form = await db.get_user_form(id_user=view_form_id)
    else:
        await view_forms.add_to_exceptions(user_id, view_form_id)
        form = await view_forms.get_next_form_for_user(user_id=user_id)

    if comment or video:

        like_and_comment = f"text:{comment.strip()}" if comment else f"video_id:{video}"
        locale = await db.get_language_user(id_user=view_form_id)
        i18n_view_form = t_hub.get_translator_by_locale(locale=locale)

        await view_forms.add_to_likes_and_comments_user(
            user_id=view_form_id,
            new_like_and_comment_user_id=user_id,
            comment=like_and_comment
        )

        await message.bot.send_message(
            chat_id=view_form_id,
            text=f"{i18n_view_form.view_forms_send_likes()}\n{i18n_view_form.view_forms_send_likes2()}\n/myprofile",
        )

    if not form:
        form = await db.get_user_form(id_user=user_id)

        await message.answer(text=i18n.no_forms_found())

        await exit_from_views_forms(
            user_form=form,
            tg_obj=message,
            i18n=i18n,
            view_forms=view_forms
        )

        return await state.set_state(FSMMainMenu.menu)

    await message.answer(
        text=i18n.first_view_form(),
        reply_markup=ready_reply_kb.buttons_view_forms(i18n=i18n)
    )

    await answer_user_form(
        user_form=form,
        tg_obj=message,
        i18n=i18n,
        answer_first_msg=False,
        answer_menu=False
    )

    await state.set_state(FSMViewForms.view_forms)
