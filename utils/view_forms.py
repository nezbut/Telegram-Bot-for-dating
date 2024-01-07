from database import MongoDB

from aiogram.fsm.storage.redis import Redis


class ViewForms:

    def __init__(self, database: MongoDB, redis: Redis) -> None:
        self.db = database
        self.redis = redis
        self.excluded_key = "excluded_forms_for"
        self.view_forms_key = "view_form"
        self.view_likes_forms_key = "view_like"
        self.last_view_form_key = "last_view_form"
        self.likes_key = "likes"
        self.likes_and_comments_key = "likes_and_comments"

    async def get_next_form_for_user(self, user_id: int) -> dict[str, str | int] | None:

        user_form = await self.db.get_user_form(id_user=user_id)

        if last_view_form_id := await self._get_last_view_form(user_id=user_id):

            last_view_form = await self.db.get_user_form(id_user=last_view_form_id)
            await self.redis.delete(f"{self.last_view_form_key}:{user_id}")

            if self._filter_form(form=last_view_form, user_form=user_form):
                await self._set_view_form(user_id=user_id, view_form_id=last_view_form_id)

                return last_view_form

        exceptions_ids: list[int] = await self._get_exceptions_user(user_id=user_id)
        exceptions_ids.append(user_id)

        forms = self.db.get_all_user_forms_excluding_users(exclud_id_users=exceptions_ids)

        async for users_form in forms:

            if self._filter_form(form=users_form, user_form=user_form):
                await self._set_view_form(user_id=user_id, view_form_id=users_form["_id"])
                return users_form

    async def clear(self, user_id: int, view_form_id: int) -> None:
        await self.redis.delete(f"{self.excluded_key}:{user_id}")
        await self.redis.delete(f"{self.view_forms_key}:{user_id}")

        if view_form_id:
            await self.redis.set(f"{self.last_view_form_key}:{user_id}", view_form_id)

    async def add_to_exceptions(self, user_id: int, *new_add_users_ids: int) -> None:

        if not await self.redis.exists(f"{self.excluded_key}:{user_id}"):
            await self.redis.lpush(f"{self.excluded_key}:{user_id}", *new_add_users_ids)
            return await self.redis.expire(name=f"{self.excluded_key}:{user_id}", time=1800)

        await self.redis.lpush(f"{self.excluded_key}:{user_id}", *new_add_users_ids)

    async def get_view_form_user(self, user_id: int) -> int | None:
        view_form = await self.redis.get(f"{self.view_forms_key}:{user_id}")

        if view_form:
            return int(view_form)

    async def add_to_likes_user(self, user_id: int, new_like_user_id: int) -> None:
        if not await self._element_in_list(
            list_key=f"{self.likes_key}:{user_id}",
            element=str(new_like_user_id)
        ) and not await self._element_in_list(
            list_key=f"{self.likes_and_comments_key}:{user_id}",
            element=str(new_like_user_id)
        ):

            await self.redis.lpush(f"{self.likes_key}:{user_id}", new_like_user_id)

    async def add_to_likes_and_comments_user(self, user_id: int, new_like_and_comment_user_id: int, comment: str) -> None:
        if not await self._element_in_list(
            list_key=f"{self.likes_and_comments_key}:{user_id}",
            element=str(new_like_and_comment_user_id)
        ) and not await self._element_in_list(
            list_key=f"{self.likes_key}:{user_id}",
            element=str(new_like_and_comment_user_id)
        ):

            await self.redis.lpush(f"{self.likes_and_comments_key}:{user_id}", f"{new_like_and_comment_user_id}:{comment}")

    async def get_next_form_like_user(self, user_id: int) -> dict[str, str | int] | None:
        next_like_user_id: bytes | None = await self.redis.lpop(f"{self.likes_and_comments_key}:{user_id}")

        if not next_like_user_id:
            next_like_user_id: bytes | None = await self.redis.lpop(f"{self.likes_key}:{user_id}")

        if next_like_user_id:
            lst = next_like_user_id.decode().split(":")
            like_id = int(lst.pop(0))

            next_like_form = await self.db.get_user_form(id_user=like_id)

            if lst:
                like_comment = ":".join(lst)
                next_like_form["like_comment"] = like_comment.strip()

            await self._set_view_like_form_user(user_id=user_id, new_view_like_form=like_id)
            return next_like_form

        await self._delete_view_like_form_user(user_id=user_id)

    async def get_view_like_form_user(self, user_id: int) -> int | None:
        view_like_form_id = await self.redis.get(f"{self.view_likes_forms_key}:{user_id}")

        if view_like_form_id:
            return int(view_like_form_id)

    async def _set_view_like_form_user(self, user_id: int, new_view_like_form: int) -> None:
        await self.redis.set(f"{self.view_likes_forms_key}:{user_id}", new_view_like_form)

    async def _delete_view_like_form_user(self, user_id: int) -> None:
        await self.redis.delete(f"{self.view_likes_forms_key}:{user_id}")

    async def get_len_likes_user(self, user_id: int) -> int:
        len_likes_user = await self.redis.llen(name=f"{self.likes_key}:{user_id}")
        len_likes_and_comments_user = await self.redis.llen(name=f"{self.likes_and_comments_key}:{user_id}")

        return len_likes_user + len_likes_and_comments_user

    async def _set_view_form(self, user_id: int, view_form_id: int) -> None:
        await self.redis.set(f"{self.view_forms_key}:{user_id}", view_form_id)

    async def _get_exceptions_user(self, user_id: int) -> list[int]:
        exceptions_ids: list[bytes] = await self.redis.lrange(f"{self.excluded_key}:{user_id}", 0, -1)

        return list(map(lambda a: int(a.decode()), exceptions_ids))

    async def _element_in_list(self, list_key: str, element: str) -> bool:
        array = map(lambda x: x.decode(), await self.redis.lrange(list_key, 0, -1))

        for elem in array:
            if element in elem:
                return True

        return False

    async def _get_last_view_form(self, user_id: int) -> int | None:
        last_view_form_id = await self.redis.get(f"{self.last_view_form_key}:{user_id}")

        if last_view_form_id:
            return int(last_view_form_id)

    def _filter_form(self, form: dict[str, str | int], user_form: dict[str, str | int]) -> bool:

        user_form_status = user_form["form_status"]
        form_status = form["form_status"]

        if user_form_status == "off" or form_status == "off":
            return False

        confirming_dict = {"age": False, "interested_in_gender": False, "city": False}

        user_age = user_form["age"]
        age = form["age"]
        user_interested_in_gender = user_form["interested_in_gender"].lower().strip()
        gender = form["gender"].lower().strip()
        user_city = user_form["city"].lower().strip()
        city = form["city"].lower().strip()

        if abs(age - user_age) <= 1:
            confirming_dict["age"] = True

        if user_interested_in_gender == "no_matter" or user_interested_in_gender[:-1] == gender:
            confirming_dict["interested_in_gender"] = True

        if user_city in city:
            confirming_dict["city"] = True

        return all(list(confirming_dict.values()))

__all__ = (
    'ViewForms',
)
