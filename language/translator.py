from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub

from .languages_tags import Languages
from .all_languages import LANGUAGES
from utils import WORK_DIR_PATH

DIR_TO_LOCALES = WORK_DIR_PATH / 'language' / 'locales'

def getTranslator() -> TranslatorHub:
    return TranslatorHub(
        locales_map={
            Languages.EN: (Languages.EN, Languages.RU),
            Languages.RU: (Languages.RU, Languages.EN)
        },

        translators=[
            FluentTranslator(
                locale=lang,
                translator=FluentBundle.from_files(locale=lang_tag, filenames=[str(DIR_TO_LOCALES / f"{lang}.ftl")])
            ) for lang, lang_tag in LANGUAGES.values()
        ],

        root_locale=Languages.RU
    )

__all__ = (
    'getTranslator',
)
