"""
Turns a cut-out photo (transparent background PNG) into the ASCII portrait used
by the neofetch card. Run once whenever you change the photo:

    pip install pillow rembg onnxruntime
    python assets/ascii.py path/to/photo.jpg

A photo with a plain background works best; the background is removed for you.

Writes assets/avatar-ascii.json, which assets/neofetch.py reads.
"""
import colorsys
import json
import sys
from pathlib import Path

from PIL import Image, ImageEnhance

COLS = 124
ART_W, LINE_H = 500, 6.7            # must match neofetch.py (width in px, line height)
CROP = None                         # (left, top, right, bottom) or None = auto-fit the figure
RAMP = " .'`:;,!|ijl1rtfkx*+=?#%&$8@MW"   # light ink -> heavy ink
OUT = Path(__file__).resolve().parent / "avatar-ascii.json"

# Tokyo Night inspired colours: warm tones for skin, cool greys for clothes
WARM = ["#7a4a30", "#b0643a", "#d9844a", "#f0a868", "#ffd2a0"]
COOL = ["#2a3150", "#414868", "#6b7394", "#a9b1d6", "#d5dbf5"]


def main(src):
    im = Image.open(src).convert("RGBA")
    if im.getextrema()[3][0] == 255:  # no transparency yet: cut the background out
        from rembg import remove, new_session
        im = remove(im, session=new_session("u2net_human_seg"))
    im = im.crop(CROP or im.getchannel("A").point(lambda a: 255 if a > 110 else 0).getbbox())
    ROWS = round(im.height / im.width * COLS * (ART_W / COLS) / LINE_H)
    im = im.resize((COLS, ROWS), Image.LANCZOS)
    # Skin and clothes are equalised separately: on a dark card the (darker) face
    # would otherwise fade out next to a white shirt.
    def is_warm(r, g, b):
        h, _, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        l = 0.299 * r + 0.587 * g + 0.114 * b
        return sat > 0.18 and (h < 0.12 or h > 0.95) and 55 < l < 200

    pix = [p for p in im.get_flattened_data() if p[3] >= 110] if hasattr(im, "get_flattened_data") \
        else [p for p in im.getdata() if p[3] >= 110]
    lum_of = lambda r, g, b: 0.299 * r + 0.587 * g + 0.114 * b
    warm_l = sorted(lum_of(*p[:3]) for p in pix if is_warm(*p[:3]))
    cool_l = sorted(lum_of(*p[:3]) for p in pix if not is_warm(*p[:3]))

    def rank(arr, v):
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] < v: lo = mid + 1
            else: hi = mid
        return lo / max(1, len(arr))
    rows = []
    for y in range(ROWS):
        runs, cur_c, cur_t = [], None, ""
        for x in range(COLS):
            r, g, b, a = im.getpixel((x, y))
            if a < 200:  # drop the soft edge so no white halo from the old background
                ch, col = " ", None
            else:
                raw = lum_of(r, g, b)
                warm = is_warm(r, g, b)
                lum = 0.42 + 0.57 * rank(warm_l, raw) if warm else 0.1 + 0.72 * rank(cool_l, raw)
                ch = RAMP[min(len(RAMP) - 1, int(lum * len(RAMP)))]
                if ch == " ":
                    ch = "."
                pal = WARM if warm else COOL
                col = pal[min(len(pal) - 1, int(lum * len(pal)))]
            if col != cur_c and cur_t:
                runs.append([cur_c, cur_t])
                cur_t = ""
            cur_c = col if ch != " " else cur_c
            cur_t += ch
        if cur_t:
            runs.append([cur_c, cur_t])
        rows.append(runs)
    OUT.write_text(json.dumps({"cols": COLS, "rows": rows}), encoding="utf-8")
    print("wrote", OUT.name)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "cutout.png")
