from aiogram import html

def give_link_to_correspondence(user_id: int, username: str | None, name: str) -> str:

    if username:
        return html.link(
            value=name,
            link=f"tg://resolve?domain={username}"
        )

    return html.link(
        value=name,
        link=f"tg://user?id={user_id}"
    )

__all__ = (
    'give_link_to_correspondence',
)
