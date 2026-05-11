import shutil
from pathlib import Path

from bs4 import BeautifulSoup

PLUGIN_STATIC_DIR = Path(__file__).parent / "static"

# Default settings, users can override in pelicanconf.py
COPY_CODE_DEFAULTS = {
    "AUTO_INJECT_ASSETS": True,
    "BUTTON_BG": None,
    "BUTTON_COLOR": None,
    "BUTTON_TEXT": "Copy",
    "COPIED_COLOR": None,
    "COPIED_TEXT": "Copied!",
    "DISPLAY": "hover",  # "hover" or "always"
    "FALLBACK_ENABLED": True,
    "OUTPUT_DIR": "copy_code",
    "TARGET_CLASS": "highlight",
    "WRAPPER_CLASS": "code-block-wrapper",
}

# Sub-directory under OUTPUT_PATH where this plugin's assets are written, and
# also the URL path segment used when referencing them from injected tags.
OUTPUT_SUBDIR = "copy_code"


def get_copy_code_settings(pelican_settings):
    """Merges user-defined settings with defaults."""
    return {
        **COPY_CODE_DEFAULTS,
        **pelican_settings.get("COPY_CODE_OPTIONS", {}),
    }

def process_code_blocks(content):
    """Process article/page content at build time.

    Wraps every <div class="highlight"> in a wrapper with a copy button.
    Handles both standard blocks and line-numbered tables. When at least one
    code block is wrapped, also injects <link> and <script> tags for the
    plugin's static assets (unless AUTO_INJECT_ASSETS is disabled).
    """
    if not content._content:
        return

    soup = BeautifulSoup(content._content, "html.parser")

    copy_code_settings = get_copy_code_settings(content.settings)
    button_bg = copy_code_settings["BUTTON_BG"]
    button_color = copy_code_settings["BUTTON_COLOR"]
    button_text = copy_code_settings["BUTTON_TEXT"]
    copied_color = copy_code_settings["COPIED_COLOR"]
    copied_text = copy_code_settings["COPIED_TEXT"]
    display = copy_code_settings["DISPLAY"]
    target_class = copy_code_settings["TARGET_CLASS"]
    wrapper_class = copy_code_settings["WRAPPER_CLASS"]
    auto_inject = copy_code_settings["AUTO_INJECT_ASSETS"]

    blocks = soup.find_all("div", class_=target_class)
    if not blocks:
        return

    for block in blocks:
        wrapper = soup.new_tag("div")
        wrapper["class"] = [wrapper_class]
        if display == "always":
            wrapper["class"].append("copy-button-always")
        block.wrap(wrapper)
        button = soup.new_tag("button")
        button["class"] = "copy-button"
        button["aria-label"] = "Copy code to clipboard"
        button.string = button_text
        wrapper.append(button)
        wrapper_styles = []
        if button_bg:
            wrapper_styles.append(f"--copy-code-button-bg: {button_bg}")
        if button_color:
            wrapper_styles.append(f"--copy-code-button-color: {button_color}")
        if copied_color:
            wrapper_styles.append(f"--copy-code-copied-color: {copied_color}")
        if wrapper_styles:
            wrapper["style"] = "; ".join(wrapper_styles)

    settings_el = soup.new_tag("div", id="copy-code-settings", hidden="")
    settings_el["data-button-text"] = copied_text
    soup.append(settings_el)

    if auto_inject:
        siteurl = content.settings.get("SITEURL", "") or ""
        base = f"{siteurl.rstrip('/')}/{OUTPUT_SUBDIR}"
        css_link = soup.new_tag(
            "link", rel="stylesheet", href=f"{base}/copy-code.css"
        )
        script_tag = soup.new_tag("script", src=f"{base}/copy-code.js")
        script_tag["defer"] = ""
        soup.append(css_link)
        soup.append(script_tag)

    content._content = str(soup)


def copy_static_files(pelican):
    """Copy bundled CSS/JS into OUTPUT_PATH/copy_code/ once the build is done."""
    output_path = pelican.settings.get("OUTPUT_PATH")
    if not output_path:
        return
    copy_code_settings = get_copy_code_settings(pelican.settings)
    dest_dir = Path(output_path) / copy_code_settings["OUTPUT_DIR"]
    dest_dir.mkdir(parents=True, exist_ok=True)
    for src_file in PLUGIN_STATIC_DIR.iterdir():
        if src_file.is_file():
            shutil.copy2(src_file, dest_dir / src_file.name)
