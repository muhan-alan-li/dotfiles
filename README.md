# dotfiles — wallpaper-driven rices

Two dark themes for Fedora 44 + KDE Plasma 6 + Ghostty, both derived from a wallpaper.

| Theme | Wallpaper | Mood |
|---|---|---|
| **Coastal** (default) | `~/Downloads/DSC03235_01.png` (Jeju coastline) | deep foliage green, shadowed sea blue, cloud grey, moss accent |
| **Sakura** | bring your own cherry blossom photo | dark plum, petal pink, cream white, soft green/blue support |

The palettes are JSON source-of-truth files. Everything else (KDE color scheme,
Ghostty config, Powerlevel10k colors) is generated from them.

## Palettes

### Coastal

| Role | Hex | Origin in photo |
|---|---|---|
| base | `#1d2819` | dark foreground foliage |
| surface | `#223946` | shadowed sea |
| surface_alt | `#2e5161` | deep teal water |
| accent | `#326f91` | open ocean blue |
| accent_bright | `#7496ac` | mid-sky blue |
| text | `#c3d0d8` | brightened cloud grey |
| muted | `#94a5b2` | soft cloud grey |
| highlight | `#888c59` | sunlit moss |

### Sakura

| Role | Hex | Note |
|---|---|---|
| base | `#1e1a1f` | dark plum |
| surface | `#2b2329` | plum panel |
| accent | `#d9879e` | deep petal pink |
| accent_bright | `#f4b8c4` | petal pink |
| text | `#fdf4f5` | cream white |
| muted | `#d9ced2` | blush grey |
| positive | `#9dbf97` | leaf green |
| link | `#a9c4d6` | sky blue |

> Sakura is a representative placeholder. Send the real photo and it will be
> re-extracted so the colors match the actual pixels.

## Layout

```
palettes/*.json        source of truth (colors + 16 ANSI roles)
kde/*.colors           generated Plasma 6 color schemes
ghostty/*.conf         generated Ghostty themes
p10k/*.zsh             generated Powerlevel10k color snippets
scripts/generate.py    palette -> config generator
scripts/apply-theme.sh install + activate a theme
wallpapers/README.md   wallpaper paths and extraction recipe
```

## Usage

### Apply a theme

```bash
cd ~/Repos/dotfiles
./scripts/apply-theme.sh coastal
# or, with a wallpaper change:
./scripts/apply-theme.sh coastal ~/Downloads/DSC03235_01.png
./scripts/apply-theme.sh sakura ~/Pictures/sakura.jpg
```

This installs all KDE schemes to `~/.local/share/color-schemes/`, copies the
selected Ghostty theme to `~/.config/ghostty/config`, applies the scheme + accent
to Plasma, and optionally sets the wallpaper. Restart Ghostty (or use its
`reload_config` action) to pick up terminal changes.

### Regenerate configs after editing a palette

```bash
python3 scripts/generate.py
./scripts/apply-theme.sh coastal   # or sakura
```

Validate the Ghostty output with:

```bash
ghostty +validate-config --config-file=ghostty/coastal.conf
```

### Powerlevel10k

Source the matching snippet in `~/.zshrc` **before** p10k loads:

```zsh
source ~/Repos/dotfiles/p10k/coastal.zsh   # or sakura.zsh
```

Your `~/.p10k.zsh` is left untouched. Run `p10k configure` if you want the
wizard to regenerate it.

## Next steps for a fuller rice

- Install theme engines so GTK/Qt apps follow the scheme:
  `sudo dnf install kvantum qt6ct qt5ct lxappearance`
- Fonts: `sudo dnf install jetbrains-mono-fonts fira-code-fonts`
- Set matching icon/cursor themes in *System Settings → Appearance*.
- Consider a tiling WM (Hyprland or Sway) only after the Plasma rice feels right.
