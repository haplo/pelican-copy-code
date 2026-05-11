# Agent Instructions: pelican-copy-code

## Project Overview

This is a Pelican namespace plugin that adds a "Copy to clipboard" button to all code blocks at build time. The plugin wraps `<div>` elements matching a configurable CSS class (default: `highlight`) in a wrapper with a copy button, and ships a small JS/CSS bundle for the clipboard interaction and styling.

## Directory Structure

```
pelican-copy-code/
├── AGENTS.md                          # This file
├── README.md                          # User-facing documentation
├── pyproject.toml                     # Package metadata & entry points
└── pelican/
    └── plugins/
        └── copy_code/
            ├── __init__.py            # Plugin registration (signals)
            ├── copy_code.py           # Core logic: HTML processing + static files
            └── static/
                ├── copy-code.css      # Button styles (hover, copied state)
                └── copy-code.js       # Clipboard interaction via navigator.clipboard
```

## Build System

- Build backend: `setuptools`
- Entry point: `pelican.plugins.copy_code`
- Dependencies: `pelican>=4.9`, `beautifulsoup4>=4.12`

## Coding Conventions

- Python 3.9+ compatible code.
- Use `pathlib.Path` for filesystem paths.
- Use `BeautifulSoup` from `bs4` for HTML manipulation.
- Keep the JS bundle small and dependency-free (no external libraries).
- CSS uses `currentColor` and `opacity` transitions for theming flexibility.

## Signal Hooks

- `content_object_init.connect(process_code_blocks)` — wraps code blocks at build time and (optionally) injects asset `<link>`/`<script>` tags into pages that contain code blocks.
- `finalized.connect(copy_static_files)` — copies the bundled CSS and JS into `{OUTPUT_PATH}/copy_code/` at the end of the build.

## Static Files Registration

Static files live in `pelican/plugins/copy_code/static/`. Pelican's `STATIC_PATHS` mechanism is **not** used because it interprets entries as paths relative to `PATH`, which produces a same-source-and-destination warning when an absolute plugin path is appended. Instead, the `finalized` signal handler copies the files directly into `{OUTPUT_PATH}/copy_code/` via `shutil.copy2`.

## Asset Auto-Injection

When at least one code block is wrapped on a page, `process_code_blocks()` appends a `<link>` to `{SITEURL}/copy_code/copy-code.css` and a deferred `<script>` to `{SITEURL}/copy_code/copy-code.js`. This means themes do not need to be modified to use the plugin. Users who want to manage asset inclusion themselves can disable this by setting `COPY_CODE["AUTO_INJECT_ASSETS"] = False`.

## Testing

No formal test suite is included in the initial version. Manual verification:
1. Install the plugin in a Pelican site.
2. Build the site with a page containing fenced code blocks.
3. Inspect the output HTML for `.code-block-wrapper` and `.copy-button` elements.
4. Click the button in a browser and confirm the clipboard content matches the code block.

## Documentation

- Keep `README.md` up-to-date when adding or changing user-facing settings, behavior, or static file paths.
- When adding a new setting, add it to the **Configuration** table (with default and description) and to the example code block in `README.md`.
