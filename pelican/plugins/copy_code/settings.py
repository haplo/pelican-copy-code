# Default settings, users can override in pelicanconf.py.
COPY_CODE_DEFAULTS = {
    "AUTO_INJECT_ASSETS": True,
    "BUTTON_BG": None,
    "BUTTON_COLOR": None,
    "BUTTON_TEXT": None,
    "COPIED_COLOR": None,
    "COPIED_TEXT": None,
    "DISPLAY": "hover",  # "hover" or "always"
    "FALLBACK_ENABLED": True,
    "OUTPUT_DIR": "copy_code",
    "TARGET_CLASS": "highlight",
    "WRAPPER_CLASS": "code-block-wrapper",
}

def get_copy_code_settings(pelican_settings):
    """Merges user-defined settings with defaults."""
    return {
        **COPY_CODE_DEFAULTS,
        **pelican_settings.get("COPY_CODE_OPTIONS", {}),
    }
