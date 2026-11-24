#!/usr/bin/env bash
# Install/apply the frosted-glass Plasma theme, blur settings and flat icons.
# This does not touch the panel layout or the color scheme.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
THEME_ID="zhelly0-glass"
THEME_DIR="${HOME}/.local/share/plasma/desktoptheme/${THEME_ID}"

"${REPO}/scripts/layout-backup.sh"

if [[ ! -d "$THEME_DIR" ]]; then
    mkdir -p "$(dirname "$THEME_DIR")"
    git clone --depth 1 https://github.com/zhelly0/glass-panel-theme "$THEME_DIR"
fi

plasma-apply-desktoptheme "$THEME_ID"

# Smooth blur without grain.
kwriteconfig6 --file kwinrc --group Effect-blur --key BlurStrength 3
kwriteconfig6 --file kwinrc --group Effect-blur --key NoiseStrength 0
gdbus call --session --dest org.kde.KWin --object-path /Effects \
    --method org.kde.kwin.Effects.reconfigureEffect blur >/dev/null 2>&1 || true

# Flat, colorful icons.
kwriteconfig6 --file kdeglobals --group Icons --key Theme Papirus
gsettings set org.gnome.desktop.interface icon-theme Papirus 2>/dev/null || true

kbuildsycoca6 --noincremental >/dev/null 2>&1 || true
systemctl --user restart plasma-plasmashell.service

echo "Applied $THEME_ID with blur and Papirus icons."
echo "To undo: plasma-apply-desktoptheme default"
