from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from filters import InstagramUrlFilter, ChangeAboutMeFilter, ChangePhotoOrVideoFilter
from database import MongoDB
from fluentogram import TranslatorRunner
from states import FSMMainMenu
from utils import answer_user_form

router = Router()

@router.message(InstagramUrlFilter())
async def insta_handlear(
    message: Message,
    instagram_url: str | None,
    state: FSMContext,
    db: MongoDB,
    i18n: TranslatorRunner
):
    id_user = message.from_user.id

    if instagram_url is not None:
        await db.update_instagram_url_user(id_user=id_user, url=instagram_url)
        await message.answer(text=i18n.done_linked_insta())

    form = await db.get_user_form(id_user=id_user)

    await answer_user_form(
        user_form=form,
        tg_obj=message,
        i18n=i18n
    )

    await state.set_state(FSMMainMenu.menu)

@router.message(ChangeAboutMeFilter())
async def change_about_me_handlear(
    message: Message,
    about_me: str,
    state: FSMContext,
    db: MongoDB,
    i18n: TranslatorRunner
):
    id_user = message.from_user.id
    form = await db.get_user_form(id_user=id_user)
    about_me = "not" if about_me.strip() == i18n.remove_about_me().strip() else about_me

    if about_me != "not_change_button":
        await db.update_form_about_me_user(id_user=id_user, new_about_me=about_me)
        form["about_me"] = about_me

    await answer_user_form(
        user_form=form,
        tg_obj=message,
        i18n=i18n
    )

    await state.set_state(FSMMainMenu.menu)

@router.message(ChangePhotoOrVideoFilter())
async def change_photo_or_video_handlear(
    message: Message,
    photo_id: str | None,
    video_id: str | None,
    no_change_button: bool,
    state: FSMContext,
    db: MongoDB,
    i18n: TranslatorRunner
):
    id_user = message.from_user.id
    form = await db.get_user_form(id_user=id_user)

    if not no_change_button:

        if photo_id:
            await db.update_form_photo_id_user(id_user=id_user, new_photo_id=photo_id)
            form["photo_id"] = photo_id

            if form.get("video_id"):
                del form["video_id"]

        else:
            await db.update_form_video_id_user(id_user=id_user, new_video_id=video_id)
            form["video_id"] = video_id

            if form.get("photo_id"):
                del form["photo_id"]

    await answer_user_form(
        user_form=form,
        tg_obj=message,
        i18n=i18n
    )

    await state.set_state(FSMMainMenu.menu)