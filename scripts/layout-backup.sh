#!/usr/bin/env bash
# Back up Plasma config before applying a layout.
set -euo pipefail

BACKUP_ROOT="${HOME}/.local/share/dotfiles-backups"
STAMP="$(date +%Y%m%d-%H%M%S)"
DEST="${BACKUP_ROOT}/${STAMP}"

mkdir -p "$DEST"
for file in plasma-org.kde.plasma.desktop-appletsrc plasmashellrc kwinrc plasmarc kdeglobals; do
    if [[ -f "${HOME}/.config/${file}" ]]; then
        cp -a "${HOME}/.config/${file}" "${DEST}/${file}"
    fi
done
printf '%s\n' "$DEST" > "${BACKUP_ROOT}/latest"

echo "Backed up Plasma config to: $DEST"
