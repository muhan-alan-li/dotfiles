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

1. **Look-and-feel theme** — a minimal rounded theme from KDE Store (e.g.
   Sweet, Catppuccin, Nordic) changes panel backgrounds, widgets and lock screen.
2. **Kvantum + GTK theme** (for app windows):
   `sudo dnf install kvantum qt6ct qt5ct lxappearance`
3. **Flat icon theme** (e.g. Papirus):
   `sudo dnf install papirus-icon-theme`
4. **Fonts**: Fira Code is the terminal font (`fira-code-fonts`, already installed)
5. **Window decorations**: KWin settings → *Window Decorations* → slim titlebar,
   small buttons, rounded corners if your theme supports them.
6. **Desktop info cards** (optional, like the red/white reference): add clock,
   calendar and system-monitor widgets directly onto the desktop rather than a
   panel, then position them in the corners.
