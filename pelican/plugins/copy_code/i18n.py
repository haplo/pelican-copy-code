import gettext
from pathlib import Path

_TRANSLATOR = None


def init_translations(locale_str):
    global _TRANSLATOR
    locale_dir = Path(__file__).parent / "i18n"
    try:
        _TRANSLATOR = gettext.translation(
            "messages", str(locale_dir), languages=[locale_str]
        )
    except FileNotFoundError:
        _TRANSLATOR = gettext.NullTranslations()


def _(s):
    if _TRANSLATOR is None:
        return s
    return _TRANSLATOR.gettext(s)