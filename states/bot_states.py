from aiogram.fsm.state import State, StatesGroup

class FSMForm(StatesGroup):
    age = State()
    gender = State()
    interested_in_gender = State()
    city = State()
    name = State()
    about_me = State()
    photo_or_video = State()
    confirmation = State()

class FSMMainMenu(StatesGroup):
    menu = State()
    language = State()
    photo_or_video_change = State()
    about_me_change = State()
    insta = State()

class FSMViewForms(StatesGroup):
    view_forms = State()
    view_like = State()
    writes_comment = State()

__all__ = (
    'FSMForm',
    'FSMMainMenu',
    'FSMViewForms'
)
