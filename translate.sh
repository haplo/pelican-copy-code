#!/usr/bin/env bash
set -euo pipefail

if ! command -v pybabel &> /dev/null; then
    echo "Error: pybabel not found. Install Babel with:" >&2
    echo "  pip install babel" >&2
    echo "  # or" >&2
    echo "  uv sync  # if Babel is in dev dependencies" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
I18N_DIR="${SCRIPT_DIR}/pelican/plugins/copy_code/i18n"
SRC_DIR="${SCRIPT_DIR}/pelican/plugins/copy_code"
POT_FILE="${I18N_DIR}/messages.pot"

cmd="${1:-}"
shift || true

case "$cmd" in
    extract)
        mkdir -p "$I18N_DIR"
        pybabel extract \
            --project=pelican-copy-code \
            --copyright-holder="Fidel Ramos" \
            --msgid-bugs-address="contact.gyldd@8shield.net" \
            -o "$POT_FILE" \
            "$SRC_DIR"
        echo "Extracted to ${POT_FILE}"
        ;;
    create)
        lang="${1:-}"
        if [ -z "$lang" ]; then
            echo "Usage: $0 create <LANG>" >&2
            exit 1
        fi
        if [ -d "${I18N_DIR}/${lang}" ]; then
            echo "Error: language '${lang}' already exists" >&2
            exit 1
        fi
        if [ ! -f "$POT_FILE" ]; then
            echo "Error: ${POT_FILE} not found. Run './translate.sh extract' first." >&2
            exit 1
        fi
        pybabel init -i "$POT_FILE" -d "$I18N_DIR" -l "$lang"
        echo "Created ${I18N_DIR}/${lang}/"
        ;;
    update)
        if [ ! -f "$POT_FILE" ]; then
            echo "Error: ${POT_FILE} not found. Run './translate.sh extract' first." >&2
            exit 1
        fi
        pybabel update -i "$POT_FILE" -d "$I18N_DIR"
        echo "Updated all .po files from ${POT_FILE}"
        ;;
    compile)
        pybabel compile -d "$I18N_DIR"
        echo "Compiled .po files to .mo in ${I18N_DIR}"
        ;;
    *)
        echo "Usage: $0 {extract|create|update|compile} [<LANG>]" >&2
        exit 1
        ;;
esac