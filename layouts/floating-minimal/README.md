# floating-minimal

A chrome-free Plasma layout inspired by the references you shared: a hairline
top strip and a centered floating dock, with everything else left as wallpaper.

## What it changes

| Area | Before | After |
|---|---|---|
| Top strip | 27 px, CPU + network monitors, clock, tray, power | 30 px, floating + translucent, clock — media — tray — power |
| Bottom dock | 46 px, launch button, pager, icons, separator, show-desktop | 48 px, centered floating pill: icons — virtual desktops — app grid |
| Media widget | buried inside the system tray | pulled out onto the top strip |
| Panels | translucent, already floating | unchanged opacity mode; just thinner and reordered |

Nothing is installed and no theme package is replaced — this is pure live
Plasma layout config, applied through `org.kde.PlasmaShell.evaluateScript`.

Note: the JS deliberately does not call `reloadConfig()` after writing
`AppletOrder` — Plasma would rewrite the order from its in-memory widget list
and undo the change.

## Apply / revert

```bash
cd ~/Repos/dotfiles
./scripts/apply-layout.sh floating-minimal   # backs up config first
./scripts/revert-layout.sh                   # restores + restarts plasmashell
```

Backups live in `~/.local/share/dotfiles-backups/<timestamp>/`.

## Manual follow-ups for the full reference look

The layout gets you the structure; these get you the "glass card" finish:

1. **Plasma style** — DONE: `apply-glass-theme.sh` installs the frosted-glass
   theme (panels/popups/toolkits), with smooth blur and no grain.
2. **Kvantum + GTK theme** (optional, for app windows):
   `sudo dnf install kvantum qt6ct qt5ct lxappearance` — then pick a matching
   theme in Kvantum Manager / lxappearance. Breeze already follows the color
   scheme, so this is optional.
3. **Flat icon theme** — DONE: Papirus (`papirus-icon-theme`).
4. **Fonts** — DONE: Fira Code is the terminal font (`fira-code-fonts`).
5. **Window decorations**: KWin settings → *Window Decorations* → slim titlebar,
   small buttons, rounded corners if your theme supports them.
6. **Desktop info cards** (optional, like the red/white reference): add clock,
   calendar and system-monitor widgets directly onto the desktop rather than a
   panel, then position them in the corners.
