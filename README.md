# pelican-copy-code

A [Pelican](https://getpelican.com/) namespace plugin that adds a **Copy to clipboard** button to all code blocks at build time.

![Screenshot of pelican-copy-code in action](https://raw.githubusercontent.com/haplo/pelican-copy-code/main/copy_code_button.webp)

## Features

- **Build-time wrapping**: the copy button is injected into HTML during Pelican's build, so there is zero client-side DOM mutation on page load.
- **Zero dependencies**: the bundled JavaScript uses the native `navigator.clipboard` API; no external libraries are required.
- **Theme-agnostic**: works with any Pelican theme that produces standard Pygments `<div class="highlight">` blocks.
- **Configurable**: optional settings in `pelicanconf.py` for button text and display behavior.

## Installation

```bash
pip install pelican-copy-code
```

The plugin should be automatically detected and enabled by Pelican. However if you define a `PLUGINS` setting in your `pelicanconf.py` then you will need to add it there:

```python
PLUGINS = ["copy_code"]
```

## Requirements

- Python >= 3.9
- Pelican >= 4.9
- beautifulsoup4 >= 4.12

## Configuration

You can control the behavior of the plugin by setting `COPY_CODE_OPTIONS` in your `pelicanconf.py`. It should be a dictionary with these keys:

| Setting              | Default                | Description                                                                                                                                                                                                  |
|----------------------|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `AUTO_INJECT_ASSETS` | `True`                 | If `True`, the plugin injects the required `<link>` and `<script>` tags into every page that has at least one wrapped code block. Set to `False` if you prefer to include the assets manually in your theme. |
| `BUTTON_BG`          | `None`                 | Background color of the copy button. `None` defaults to `#fff`.                                                                                                                                              |
| `BUTTON_COLOR`       | `None`                 | Text and border color of the copy button. `None` defaults to `#000`.                                                                                                                                         |
| `BUTTON_TEXT`        | `"Copy"`               | Text displayed on the copy button.                                                                                                                                                                           |
| `COPIED_COLOR`       | `None`                 | Text and border color of the copy button after a successful copy. Falls back to `#d9411e`.                                                                                                                   |
| `COPIED_TEXT`        | `"Copied!"`            | Text shown after a successful copy.                                                                                                                                                                          |
| `DISPLAY`            | `"hover"`              | `"hover"` or `"always"` visibility mode.                                                                                                                                                                     |
| `OUTPUT_DIR`         | `"copy_code"`          | Where to put pelican-copy-code assets inside Pelican output                                                                                                                                                  |
| `TARGET_CLASS`       | `"highlight"`          | CSS class of code block `<div>` elements to target.                                                                                                                                                          |
| `WRAPPER_CLASS`      | `"code-block-wrapper"` | CSS class applied to the wrapper `<div>` around each code block.                                                                                                                                             |

Example:

```python
COPY_CODE_OPTIONS = {
    "AUTO_INJECT_ASSETS": True,
    "BUTTON_BG": "#fff",
    "BUTTON_COLOR": "#555",
    "BUTTON_TEXT": "Copy",
    "COPIED_COLOR": "#d9411e",
    "COPIED_TEXT": "¡Copiado!",
    "DISPLAY": "hover",
    "TARGET_CLASS": "highlight",
    "WRAPPER_CLASS": "code-block-wrapper",
}
```

## Theme Integration

No theme or template changes are required. By default, the plugin:

1. Copies its bundled `copy-code.css` and `copy-code.js` into `{OUTPUT_PATH}/copy_code/` at the end of the build (`finalized` signal).
2. Injects the corresponding `<link>` and `<script>` tags into each rendered article/page that contains at least one wrapped code block.

If you would rather include the assets yourself (for example to place them in `<head>` or to bundle them with other static assets), set `COPY_CODE_OPTIONS["AUTO_INJECT_ASSETS"] = False` and add the tags to your base template:

```html
<link rel="stylesheet" href="{{ SITEURL }}/copy_code/copy-code.css">
<script src="{{ SITEURL }}/copy_code/copy-code.js" defer></script>
```

The files are always copied to `{OUTPUT_PATH}/copy_code/` regardless of the `AUTO_INJECT_ASSETS` setting.

## Internationalization (i18n)

The plugin includes compiled translations to multiple languages (see the [i18n dir](/pelican/plugins/copy_code/i18n/) for the current list). The translations will be activated automatically when using the [`DEFAULT_LANG` Pelican setting](https://docs.getpelican.com/en/latest/settings.html#DEFAULT_LANG) or when using the [i18n-subsites](https://github.com/pelican-plugins/i18n-subsites) plugin.

The `BUTTON_TEXT` and `COPIED_TEXT` settings will override the texts, they are used as-is without translation.

### Contributing a translation

You need to install [Babel](https://pypi.org/project/babel/) for its `pybabel` utility. It's a development dependency so you should have it if you did `uv sync`.

```bash
# Create a new language catalog (e.g. Czech)
./translate.sh create cz

# Edit the .po file with your translations, then compile
./translate.sh compile
```

Translation catalogs live in `pelican/plugins/copy_code/i18n/{lang}/LC_MESSAGES/`. Both `.po` and compiled `.mo` files are committed to the repository.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and building.

```bash
git clone https://github.com/haplo/pelican-copy-code.git
cd pelican-copy-code
uv sync
```

To build the package:

```bash
uv build
```

To run the plugin in a Pelican site during development, install it in editable mode into the site's virtual environment:

```bash
pip install -e /path/to/pelican-copy-code
# or with uv
uv add --editable /path/to/pelican-copy-code
```

## How It Works

1. **At build time**, `process_code_blocks()` finds every `<div>` matching the configured `TARGET_CLASS` (default: `highlight`) in article/page content and wraps it in a `<div>` with the configured `WRAPPER_CLASS` (default: `code-block-wrapper`) and appends a `<button class="copy-button">`. If `AUTO_INJECT_ASSETS` is enabled (the default), it also appends `<link>` and `<script>` tags pointing at the plugin's CSS and JS.
2. **At the end of the build**, `copy_static_files()` copies `copy-code.css` and `copy-code.js` into `{OUTPUT_PATH}/copy_code/`.
3. **At runtime**, the bundled `copy-code.js` attaches click listeners to each button. When clicked, it extracts the `textContent` of the adjacent `<pre>` element and writes it to the clipboard via `navigator.clipboard.writeText()`.

## License

MIT
