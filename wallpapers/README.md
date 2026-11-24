# Wallpapers

Image files are intentionally **not** committed (see `.gitignore`); this file just
records where each theme's wallpaper lives.

## Coastal (active default)

- Path: `/home/muhanli/Downloads/DSC03235_01.png`
- Scene: overcast Jeju coastline with wind turbines, deep blue sea and green headland.
- Palette in `palettes/coastal.json` was extracted directly from this image.

## Sakura

- Path: **TBD** — drop your cherry blossom photo somewhere (e.g. `~/Pictures/sakura.jpg`)
  and point me at it.
- Once you have it, extract a palette and update `palettes/sakura.json`, then run
  `python3 scripts/generate.py` and `./scripts/apply-theme.sh sakura /path/to/sakura.jpg`.

### Extracting a palette from a new photo

```bash
python3 - <<'EOF'
from PIL import Image
im = Image.open('/path/to/photo.jpg').convert('RGB')
im.thumbnail((400, 400))
q = im.quantize(colors=12, method=2)
pal = q.getpalette()[:36]
for count, idx in sorted(q.getcolors(), reverse=True):
    r, g, b = pal[idx*3:idx*3+3]
    print(f"#{r:02x}{g:02x}{b:02x}  {count}px")
EOF
```
