from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.methods import send_message, edit_message_text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from fluentogram import TranslatorRunner
from .view_forms import ViewForms

class MainMenuCallbackFactory(CallbackData, prefix="main_menu"):
    button: str

async def answer_main_menu(
        tg_obj: Message | CallbackQuery,
        i18n: TranslatorRunner,
        instagram: bool,
        form_status: str,
        edit: bool = False
    ) -> send_message.SendMessage | edit_message_text.EditMessageText:

    msg: Message = tg_obj if isinstance(tg_obj, Message) else tg_obj.message

    builder = InlineKeyboardBuilder()

    first_btns = [
        InlineKeyboardButton(
            text=i18n.menu.view_forms(),
            callback_data=MainMenuCallbackFactory(button="view_forms").pack()
        ),
        InlineKeyboardButton(
            text=i18n.menu.change_form(),
            callback_data=MainMenuCallbackFactory(button="change_form").pack()
        )
    ]

    builder.row(*first_btns, width=2)

    menu_btns = [
        InlineKeyboardButton(
            text=i18n.menu.change_photo_or_video(),
            callback_data=MainMenuCallbackFactory(button="change_photo_or_video").pack()
        ),

        InlineKeyboardButton(
            text=i18n.menu.change_about_me(),
            callback_data=MainMenuCallbackFactory(button="change_about_me").pack()
        ),

        InlineKeyboardButton(
            text=i18n.menu.un_insta() if instagram else i18n.menu.insta(),
            callback_data=MainMenuCallbackFactory(button="un_insta" if instagram else "insta").pack()
        ),

        InlineKeyboardButton(
            text=i18n.menu.view_like(),
            callback_data=MainMenuCallbackFactory(button="view_like").pack()
        )
    ]

    builder.row(*menu_btns, width=1)

    last_btns = [
        InlineKeyboardButton(
            text=i18n.menu.language(),
            callback_data=MainMenuCallbackFactory(button="language").pack()
        ),

        InlineKeyboardButton(
            text=i18n.menu.form_off() if form_status == "off" else i18n.menu.form_included(),
            callback_data=MainMenuCallbackFactory(button="form_included" if form_status == "off" else "form_off").pack()
        )
    ]

    builder.row(*last_btns, width=2)

    if not edit:

        return await msg.answer(
            text=i18n.menu.choice(),
            reply_markup=builder.as_markup()
        )

    return await msg.edit_text(
        text=i18n.menu.choice(),
        reply_markup=builder.as_markup()
    )

async def answer_user_form(
        user_form: dict[str, str | int],
        tg_obj: Message | CallbackQuery,
        i18n: TranslatorRunner,
        answer_first_msg=True,
        answer_menu=True
    ) -> send_message.SendMessage | edit_message_text.EditMessageText:

    msg: Message = tg_obj if isinstance(tg_obj, Message) else tg_obj.message
    inst_url = user_form.get("instagram_url")
    form_status = user_form.get("form_status")
    result_answer = None
    builder = InlineKeyboardBuilder()

    if inst_url != "not":
        builder.button(
            text="Instagram",
            url=inst_url
        )

    if answer_first_msg:
        await msg.answer(text=i18n.user_form(), reply_markup=ReplyKeyboardRemove())

    photo_id = user_form.get("photo_id")
    video_id = user_form.get("video_id")

    if user_form["about_me"] == "not":
        form = i18n.form_no_about(
            name=user_form["name"],
            age=user_form["age"],
            city=user_form["city"]
        )
    else:
        form = i18n.form(
            name=user_form["name"],
            age=user_form["age"],
            city=user_form["city"],
            about_me=user_form["about_me"]
        )

    if photo_id:
        result_answer = await msg.answer_photo(
            photo=photo_id,
            caption=form,
            reply_markup=builder.as_markup() if inst_url else None
        )
    else:
        result_answer = await msg.answer_video(
            video=video_id,
            caption=form,
            reply_markup=builder.as_markup() if inst_url else None
        )

    if answer_menu:
        result_answer = await answer_main_menu(
            tg_obj=tg_obj,
            i18n=i18n,
            instagram=False if inst_url == "not" else True,
            form_status=form_status
        )

    return result_answer

async def exit_from_views_forms(
        user_form: dict[str, str | int],
        tg_obj: Message | CallbackQuery,
        i18n: TranslatorRunner,
        view_forms: ViewForms
    ) -> send_message.SendMessage | edit_message_text.EditMessageText:

    user_id = user_form["_id"]

    await view_forms.clear(
        user_id=user_id,
        view_form_id=await view_forms.get_view_form_user(user_id=user_id)
    )

    return await answer_user_form(
        user_form=user_form,
        tg_obj=tg_obj,
        i18n=i18n
    )

async def answer_like_form(
        form: dict[str, str | int],
        tg_obj: Message | CallbackQuery,
        i18n: TranslatorRunner,
        reply_markup: ReplyKeyboardMarkup | None = None,
        answer_first_msg=True
) -> None:
    message = tg_obj if isinstance(tg_obj, Message) else tg_obj.message

    if answer_first_msg:
        await message.answer(
            text=i18n.view_likes(),
            reply_markup=reply_markup
        )

    await answer_user_form(
        user_form=form,
        tg_obj=tg_obj,
        i18n=i18n,
        answer_first_msg=False,
        answer_menu=False
    )

    like_comment = form.get("like_comment")

    if like_comment:

        if like_comment.startswith("text:"):
            text_comment = like_comment.removeprefix("text:")

            await message.answer(
                text=f"{i18n.view_forms_btns.like_and_comment()}: {text_comment}"
            )

        else:
            video_id_comment = like_comment.removeprefix("video_id:")
            await message.answer_video(
                video=video_id_comment,
                caption=i18n.view_forms_btns.like_and_comment()
            )

__all__ = (
    'answer_main_menu',
    'answer_user_form',
    'exit_from_views_forms',
    'answer_like_form',
    'MainMenuCallbackFactory'
)
