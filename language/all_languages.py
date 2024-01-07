from .languages_tags import Languages, LanguagesTags

LANGUAGES: dict[str, tuple[str]] = {
    "🇷🇺 Русский": (Languages.RU, LanguagesTags.RU),
    "🇬🇧 English": (Languages.EN, LanguagesTags.EN)
}

__all__ = (
    'LANGUAGES',
)
