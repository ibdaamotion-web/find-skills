"""Split one generated collage (3 scenes stacked top->bottom: liver, kidney, H. pylori)
into img/liver.jpg, img/kidney.jpg, img/hpylori.jpg.

Usage: python3 split_collage.py path/to/collage.png
- Finds the light separator lines between panels; falls back to equal thirds.
- Trims leftover border, upscales each panel to >= 1600 px wide (Lanczos) for the 1080 px post.
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps, ImageStat

KEYS = ["liver", "kidney", "hpylori"]
OUT = Path(__file__).parent / "img"


def separator_rows(im):
    g = ImageOps.grayscale(im)
    w, h = g.size
    rows = []
    for y in range(h):
        st = ImageStat.Stat(g.crop((0, y, w, y + 1)))
        # near-uniform row (white/black gutter)
        if st.stddev[0] < 6 and (st.mean[0] > 235 or st.mean[0] < 20):
            rows.append(y)
    return rows


def find_cuts(im):
    h = im.size[1]
    rows = set(separator_rows(im))
    cuts = []
    for target in (h / 3, 2 * h / 3):
        window = [y for y in rows if abs(y - target) < h * 0.08]
        if window:
            # middle of the contiguous gutter nearest to target
            y = min(window, key=lambda v: abs(v - target))
            lo = hi = y
            while lo - 1 in rows:
                lo -= 1
            while hi + 1 in rows:
                hi += 1
            cuts.append((lo, hi + 1))
        else:
            cuts.append((round(target), round(target)))
    return [(0, cuts[0][0]), (cuts[0][1], cuts[1][0]), (cuts[1][1], h)]


def trim(im):
    g = ImageOps.grayscale(im)
    w, h = g.size
    def uniform(box):
        st = ImageStat.Stat(g.crop(box))
        return st.stddev[0] < 6 and (st.mean[0] > 235 or st.mean[0] < 20)
    l, t, r, b = 0, 0, w, h
    while l < w // 4 and uniform((l, 0, l + 1, h)): l += 1
    while r > w * 3 // 4 and uniform((r - 1, 0, r, h)): r -= 1
    while t < h // 4 and uniform((0, t, w, t + 1)): t += 1
    while b > h * 3 // 4 and uniform((0, b - 1, w, b)): b -= 1
    return im.crop((l, t, r, b))


def main(src):
    im = Image.open(src).convert("RGB")
    OUT.mkdir(exist_ok=True)
    for key, (y0, y1) in zip(KEYS, find_cuts(im)):
        panel = trim(im.crop((0, y0, im.size[0], y1)))
        if panel.width < 1600:
            s = 1600 / panel.width
            panel = panel.resize((1600, round(panel.height * s)), Image.LANCZOS)
        dst = OUT / f"{key}.jpg"
        panel.save(dst, quality=94)
        print(f"{key}: rows {y0}-{y1} -> {dst.name} {panel.size}")


if __name__ == "__main__":
    main(sys.argv[1])
