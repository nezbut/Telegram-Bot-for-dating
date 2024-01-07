from motor.core import AgnosticDatabase, AgnosticCursor
from pymongo.errors import DuplicateKeyError
from typing import Any

class MongoDB:

    def __init__(self, db: AgnosticDatabase) -> None:
        self.db = db
        self.users_coll = db.users
        self.users_forms_coll = db.users_forms

    async def insert_user(self, id_user: int, name_user: str, lang_code: str, username: str | None = None) -> bool:

        pattern = {
            "_id": id_user,
            "name": name_user,
            "language_code": lang_code
        }

        if username:
            pattern["username"] = username

        try:
            await self.users_coll.insert_one(pattern)

        except DuplicateKeyError:
            return False

        else:
            return True

    async def insert_user_form(
        self,
        id_user: int,
        age: int,
        gender: str,
        interested_in_gender: str,
        city: str,
        name: str,
        about_me: str,
        photo_id: str | None = None,
        video_id: str | None = None
    ) -> bool:

        pattern = {
            "_id": id_user,
            "age": age,
            "gender": gender,
            "interested_in_gender": interested_in_gender,
            "city": city,
            "name": name,
            "about_me": about_me,
            "form_status": "included",
            "instagram_url": "not"
        }

        if photo_id:
            pattern['photo_id'] = photo_id

        elif video_id:
            pattern['video_id'] = video_id

        else:
            return False

        try:
            await self.users_forms_coll.insert_one(pattern)

        except DuplicateKeyError:
            return False

        else:
            return True

    def get_all_user_forms_excluding_users(self, exclud_id_users: list[int]) -> AgnosticCursor:
        return self.users_forms_coll.find(
            {
                "_id": {"$nin": exclud_id_users}
            }
        )

    async def get_language_user(self, id_user: int) -> str:
        lang = await self.users_coll.find_one({"_id": id_user})

        if lang:
            return lang['language_code'].lower().strip()

    async def get_user_form(self, id_user: int) -> dict[str, str | int] | None:
        user_form = await self.users_forms_coll.find_one({"_id": id_user})
        return user_form

    async def get_username(self, id_user: int) -> str | None:
        user = await self.users_coll.find_one({"_id": id_user})

        if user:
            return user.get("username")

    async def update_user_form(self, id_user: int, **kwargs) -> bool:
        data_in_update: dict[str, dict[str, str | int]] = {"$set": {key: value for key, value in kwargs.items() if value != "not_change_button"}}
        data_in_update["$unset"] = {f"{'photo_id' if kwargs.get('video_id') else 'video_id'}": ""}

        result = await self.users_forms_coll.update_one(
            {"_id": id_user},
            data_in_update
        )

        return bool(result.matched_count or result.modified_count)

    async def _update_user_form_collection(self, id_user: int, set_key: str, value: Any, unset_key: str | None = None, unset_value: Any = None) -> bool:
        data_to_update = {
            "$set": {set_key: value}
        }

        if unset_key:
            data_to_update.update(
                {
                    "$unset": {unset_key: unset_value}
                }
            )

        result = await self.users_forms_coll.update_one(
            {"_id": id_user},
            data_to_update
        )

        return bool(result.matched_count or result.modified_count)

    async def update_language_user(self, id_user: int, new_lang_code: str) -> bool:
        data_to_update = {
            "$set": {"language_code": new_lang_code}
        }

        result = await self.users_coll.update_one(
            {"_id": id_user},
            data_to_update
        )

        return result

    async def update_form_status_user(self, id_user: int, new_status: str = "off") -> bool:
        result = await self._update_user_form_collection(
            id_user=id_user,
            set_key="form_status",
            value=new_status
        )

        return result

    async def update_form_photo_id_user(self, id_user: int, new_photo_id: str) -> bool:
        result = await self._update_user_form_collection(
            id_user=id_user,
            set_key="photo_id",
            value=new_photo_id,
            unset_key="video_id",
            unset_value=""
        )

        return result

    async def update_form_video_id_user(self, id_user: int, new_video_id: str) -> bool:
        result = await self._update_user_form_collection(
            id_user=id_user,
            set_key="video_id",
            value=new_video_id,
            unset_key="photo_id",
            unset_value=""
        )

        return result

    async def update_form_about_me_user(self, id_user: int, new_about_me: str) -> bool:
        result = await self._update_user_form_collection(
            id_user=id_user,
            set_key="about_me",
            value=new_about_me
        )

        return result

    async def update_instagram_url_user(self, id_user: int, url: str) -> bool:
        result = await self._update_user_form_collection(
            id_user=id_user,
            set_key="instagram_url",
            value=url
        )

        return result

    async def exists_user(self, id_user: int) -> bool:
        is_exists = await self.users_coll.count_documents({"_id": id_user})
        return bool(is_exists)

    async def exists_user_form(self, id_user: int) -> bool:
        is_exists = await self.users_forms_coll.count_documents({"_id": id_user})
        return bool(is_exists)

__all__ = (
    'MongoDB',
)
