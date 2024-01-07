from .form_fill_filters import AboutMeChoiceFilter, PhotoOrVideoChoiceFilter
from states import FSMMainMenu

class ChangeAboutMeFilter(AboutMeChoiceFilter):
    filter_state = FSMMainMenu.about_me_change.state

class ChangePhotoOrVideoFilter(PhotoOrVideoChoiceFilter):
    filter_state = FSMMainMenu.photo_or_video_change.state

__all__ = (
    'ChangeAboutMeFilter',
    'ChangePhotoOrVideoFilter'
)
