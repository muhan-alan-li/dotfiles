#!/usr/bin/env bash
# Apply a theme from this repo to the live KDE Plasma session and Ghostty.
#
# Usage: ./scripts/apply-theme.sh coastal|sakura [optional-wallpaper-path]
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
    echo "Usage: $(basename "$0") coastal|sakura [wallpaper-image]" >&2
    exit 1
}

THEME="${1:-}"
[[ -n "$THEME" ]] || usage
case "$THEME" in
    coastal|sakura) ;;
    *) echo "Unknown theme: $THEME (choose coastal or sakura)" >&2; usage ;;
esac

PALETTE="$REPO/palettes/$THEME.json"
[[ -f "$PALETTE" ]] || { echo "Missing palette: $PALETTE" >&2; exit 1; }

SCHEME="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["name"])' "$PALETTE")"
ACCENT="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["colors"]["accent"])' "$PALETTE")"

mkdir -p "$HOME/.local/share/color-schemes" "$HOME/.config/ghostty"

# Install all schemes so switching between themes always works.
for file in "$REPO"/kde/*.colors; do
    install -m 644 "$file" "$HOME/.local/share/color-schemes/$(basename "$file")"
done

# Install the selected Ghostty config.
install -m 644 "$REPO/ghostty/$THEME.conf" "$HOME/.config/ghostty/config"

# Apply to Plasma. These must be separate calls: combining --accent-color with a
# scheme name only applies the accent on this Plasma version.
plasma-apply-colorscheme "$SCHEME"
plasma-apply-colorscheme --accent-color "$ACCENT"

# Optionally apply a wallpaper too.
WALLPAPER="${2:-}"
if [[ -n "$WALLPAPER" ]]; then
    if [[ -f "$WALLPAPER" ]]; then
        plasma-apply-wallpaperimage "$WALLPAPER"
    else
        echo "Warning: wallpaper not found, skipped: $WALLPAPER" >&2
    fi
fi

echo "Applied '$THEME' (KDE scheme: $SCHEME, accent: $ACCENT)."
echo "Ghostty config written to ~/.config/ghostty/config - restart Ghostty or use its reload_config action."
