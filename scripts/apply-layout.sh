#!/usr/bin/env bash
# Apply a layout from layouts/<name>/apply.js to the live Plasma session.
#
# Usage: ./scripts/apply-layout.sh [layout-name]   (default: floating-minimal)
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LAYOUT="${1:-floating-minimal}"
JS="${REPO}/layouts/${LAYOUT}/apply.js"

if [[ ! -f "$JS" ]]; then
    echo "No such layout: $LAYOUT (expected $JS)" >&2
    exit 1
fi
if ! command -v gdbus >/dev/null 2>&1; then
    echo "gdbus is required" >&2
    exit 1
fi

"${REPO}/scripts/layout-backup.sh"

echo "Applying layout '$LAYOUT'..."
gdbus call --session \
    --dest org.kde.plasmashell \
    --object-path /PlasmaShell \
    --method org.kde.PlasmaShell.evaluateScript \
    "$(cat "$JS")"

echo "Done. Revert with: ${REPO}/scripts/revert-layout.sh"
