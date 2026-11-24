#!/usr/bin/env bash
# Restore the Plasma config snapshot taken by layout-backup.sh.
# This briefly restarts plasmashell.
set -euo pipefail

BACKUP_ROOT="${HOME}/.local/share/dotfiles-backups"
LATEST="${BACKUP_ROOT}/latest"

if [[ ! -f "$LATEST" ]]; then
    echo "No backup found - nothing to revert." >&2
    exit 1
fi
DEST="$(cat "$LATEST")"
if [[ ! -d "$DEST" ]]; then
    echo "Backup directory missing: $DEST" >&2
    exit 1
fi

echo "Restoring from: $DEST"
systemctl --user stop plasma-plasmashell.service
cp -a "${DEST}"/. "${HOME}/.config/"
systemctl --user start plasma-plasmashell.service

echo "Reverted. plasmashell restarted."
