#!/usr/bin/env python3
"""Generate KDE, Ghostty and Powerlevel10k configs from palettes/*.json.

Usage: python3 scripts/generate.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PALETTES = ROOT / "palettes"


def rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    return f"{int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)}"


def role_block(c: dict, sel_fg: str, alternate: str, normal: str) -> list[str]:
    return [
        f"BackgroundAlternate={rgb(c[alternate])}",
        f"BackgroundNormal={rgb(c[normal])}",
        f"DecorationFocus={rgb(c['accent'])}",
        f"DecorationHover={rgb(c['accent'])}",
        f"ForegroundActive={rgb(c['accent_bright'])}",
        f"ForegroundInactive={rgb(c['muted'])}",
        f"ForegroundLink={rgb(c['link'])}",
        f"ForegroundNegative={rgb(c['negative'])}",
        f"ForegroundNeutral={rgb(c['warning'])}",
        f"ForegroundNormal={rgb(sel_fg)}",
        f"ForegroundPositive={rgb(c['positive'])}",
        f"ForegroundVisited={rgb(c['accent_bright'])}",
    ]


def write_colors(name: str, p: dict) -> None:
    c = p["colors"]
    a = p["ansi"]
    sel_fg = p["selection_fg"]
    lines = [
        f"# {name} color scheme - generated from palettes/{p['slug']}.json",
        "# Do not edit by hand; edit the palette and re-run scripts/generate.py.",
        "",
        "[ColorEffects:Disabled]",
        f"Color={rgb(c['muted'])}",
        "ColorAmount=0",
        "ColorEffect=0",
        "ContrastAmount=0.65",
        "ContrastEffect=1",
        "IntensityAmount=0.1",
        "IntensityEffect=2",
        "",
        "[ColorEffects:Inactive]",
        "ChangeSelectionColor=true",
        f"Color={rgb(c['muted'])}",
        "ColorAmount=0.025",
        "ColorEffect=2",
        "ContrastAmount=0.1",
        "ContrastEffect=2",
        "Enable=false",
        "IntensityAmount=0",
        "IntensityEffect=0",
        "",
    ]

    sections = [
        ("Colors:Button", "surface_alt", "surface"),
        ("Colors:Complementary", "surface", "base"),
        ("Colors:Header", "surface", "surface_alt"),
        ("Colors:Header][Inactive", "surface_alt", "surface"),
        ("Colors:Tooltip", "surface", "surface_alt"),
        ("Colors:View", "surface_alt", "base"),
        ("Colors:Window", "surface", "surface"),
    ]
    for section, alternate, normal in sections:
        lines += [f"[{section}]"] + role_block(c, sel_fg, alternate, normal) + [""]

    lines += [
        "[Colors:Selection]",
        f"BackgroundAlternate={rgb(c['surface_alt'])}",
        f"BackgroundNormal={rgb(c['accent'])}",
        f"DecorationFocus={rgb(c['accent'])}",
        f"DecorationHover={rgb(c['accent'])}",
        f"ForegroundActive={rgb(sel_fg)}",
        f"ForegroundInactive={rgb(c['muted'])}",
        f"ForegroundLink={rgb(c['link'])}",
        f"ForegroundNegative={rgb(c['negative'])}",
        f"ForegroundNeutral={rgb(c['warning'])}",
        f"ForegroundNormal={rgb(sel_fg)}",
        f"ForegroundPositive={rgb(c['positive'])}",
        f"ForegroundVisited={rgb(c['accent_bright'])}",
        "",
        "[General]",
        f"ColorScheme={name}",
        f"Name={name}",
        "shadeSortColumn=true",
        "",
    ]

    out = ROOT / "kde" / f"{name}.colors"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")


def write_ghostty(p: dict) -> None:
    c = p["colors"]
    a = p["ansi"]
    lines = [
        f"# {p['name']} - generated from palettes/{p['slug']}.json",
        "# Do not edit by hand; edit the palette and re-run scripts/generate.py.",
        "",
        f"background = {c['base']}",
        f"foreground = {c['text']}",
        f"cursor-color = {p['cursor']}",
        f"selection-background = {p['selection_bg']}",
        f"selection-foreground = {p['selection_fg']}",
        "",
    ]
    for i in range(16):
        key = list(a)[i]
        lines.append(f"palette = {i}={a[key]}")
    lines += [
        "",
        "font-size = 12",
        "window-padding-x = 12",
        "window-padding-y = 12",
        "background-opacity = 1.0",
        "",
    ]
    out = ROOT / "ghostty" / f"{p['slug']}.conf"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")


def write_p10k(p: dict) -> None:
    a = p["ansi"]
    lines = [
        f"# {p['name']} Powerlevel10k palette - generated from palettes/{p['slug']}.json",
        "# Source this file in ~/.zshrc BEFORE powerlevel10k is loaded.",
        "# Do not edit by hand; edit the palette and re-run scripts/generate.py.",
        "",
        "POWERLEVEL9K_COLOR_SCHEME='dark'",
        "POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(dir vcs)",
        "POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status time)",
        f"POWERLEVEL9K_DIR_FOREGROUND='{a['bright_blue']}'",
        f"POWERLEVEL9K_VCS_CLEAN_FOREGROUND='{a['green']}'",
        f"POWERLEVEL9K_VCS_MODIFIED_FOREGROUND='{a['yellow']}'",
        f"POWERLEVEL9K_VCS_UNTRACKED_FOREGROUND='{a['red']}'",
        f"POWERLEVEL9K_STATUS_OK_FOREGROUND='{a['green']}'",
        f"POWERLEVEL9K_STATUS_ERROR_FOREGROUND='{a['red']}'",
        f"POWERLEVEL9K_TIME_FOREGROUND='{a['white']}'",
        "",
    ]
    out = ROOT / "p10k" / f"{p['slug']}.zsh"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")


def main() -> None:
    for path in sorted(PALETTES.glob("*.json")):
        p = json.loads(path.read_text(encoding="utf-8"))
        p.setdefault("slug", path.stem)
        write_colors(p["name"], p)
        write_ghostty(p)
        write_p10k(p)


if __name__ == "__main__":
    main()
