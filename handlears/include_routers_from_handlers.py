from aiogram import Router

from .messages import (
    commands_handlears,
    fills_form,
    menu_handlears,
    other_messages,
    view_forms_handlears,
    view_likes_handlears
)
from .callbacks import (
    fills_form_callbacks,
    main_menu_buttons_callbacks,
    other_callbacks
)

def getRouters() -> list[Router]:
    routers = [
        commands_handlears.router,
        view_forms_handlears.router,
        view_likes_handlears.router,
        fills_form.router,
        menu_handlears.router,
        fills_form_callbacks.router,
        main_menu_buttons_callbacks.router,
        other_messages.router,
        other_callbacks.router
    ]

    return routers

__all__ = (
    'getRouters',
)
