from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import or_f

from fluentogram import TranslatorRunner, TranslatorHub

from filters import (
    ViewLikesLikeFilter,
    ViewLikesDislikeFilter,
    ViewLikesContinueFilter
)

from database import MongoDB

from utils import (
    answer_user_form,
    ViewForms,
    answer_like_form,
    give_link_to_correspondence
)

from states import FSMMainMenu
from keyboards import ReadyReplyKeyboards

router = Router()

@router.message(ViewLikesLikeFilter())
async def view_likes_like(
    message: Message,
    view_forms: ViewForms,
    i18n: TranslatorRunner,
    t_hub: TranslatorHub,
    db: MongoDB,
    ready_reply_kb: ReadyReplyKeyboards
):
    user_id = message.from_user.id
    view_like_id = await view_forms.get_view_like_form_user(user_id=user_id)

    user_form = await db.get_user_form(id_user=user_id)
    view_like_form = await db.get_user_form(id_user=view_like_id)

    user_username = await db.get_username(id_user=user_id)
    view_like_username = await db.get_username(id_user=view_like_id)

    locale = await db.get_language_user(id_user=view_like_id)
    i18n_view_like = t_hub.get_translator_by_locale(locale=locale.lower().strip())

    await message.answer(
        text=f"{i18n.hope_good_time()}\n{i18n.have_nice_chat()} {give_link_to_correspondence(user_id=view_like_id, username=view_like_username, name=view_like_form['name'])}", # !!!!!!!!!!!!
        reply_markup=ready_reply_kb.one_button(text=i18n.contin())
    )

    await message.bot.send_message(
        chat_id=view_like_id,
        text=f"{i18n_view_like.mutual_sympathy()}\n{i18n_view_like.have_nice_chat()} {give_link_to_correspondence(user_id=user_id, username=user_username, name=user_form['name'])}"
    )

@router.message(or_f(ViewLikesDislikeFilter(), ViewLikesContinueFilter()))
async def view_likes_dislike(
    message: Message,
    view_forms: ViewForms,
    i18n: TranslatorRunner,
    db: MongoDB,
    state: FSMContext,
    ready_reply_kb: ReadyReplyKeyboards
):
    user_id = message.from_user.id
    next_like_form = await view_forms.get_next_form_like_user(user_id=user_id)

    if next_like_form:
        result_for_continue = message.text.strip() == i18n.contin().strip()

        return await answer_like_form(
            form=next_like_form,
            tg_obj=message,
            i18n=i18n,
            answer_first_msg=result_for_continue,
            reply_markup=ready_reply_kb.buttons_view_likes(i18n=i18n) if result_for_continue else None
        )

    user_form = await db.get_user_form(id_user=user_id)
    await answer_user_form(
        user_form=user_form,
        tg_obj=message,
        i18n=i18n
    )

    await state.set_state(FSMMainMenu.menu)
