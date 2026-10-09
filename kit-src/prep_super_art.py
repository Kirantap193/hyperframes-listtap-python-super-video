"""Prepare the user's super() artwork (2026-10-09).

1.webp  pizza / burger price cards (already transparent)  -> g4-pizza.png, g4-burger.png
3.webp  Types of Inheritance (checkerboard baked in)       -> g8-types.png (transparent),
        g8-types-plate.png (same art, label text removed), g8-types-text.json (text boxes + letter cuts)
"""
import json, pathlib, shutil
import numpy as np
from PIL import Image
from scipy import ndimage
import cv2

SRC = pathlib.Path(r"C:\Users\kiran\AppData\Local\Temp\claude\C--Users-kiran-OneDrive-Desktop-StoryBoard\42f6b862-d430-4d77-ae14-eef188485265\images")
ASSET = pathlib.Path(r"C:\Users\kiran\OneDrive\Asset's\Super")
OUT = pathlib.Path(r"C:\Users\kiran\Documents\hyperframes\video-15-parts")
ASSET.mkdir(exist_ok=True)

# ---------- pizza / burger ----------
shutil.copy2(SRC / "1.webp", ASSET / "price-cards-pizza-500-burger-250.webp")
im = Image.open(SRC / "1.webp").convert("RGBA")
a = np.array(im)[:, :, 3]
cols = np.where(a.max(axis=0) > 8)[0]
gaps = np.where(np.diff(cols) > 20)[0]
split = (cols[gaps[0]] + cols[gaps[0] + 1]) // 2
for name, box in (("pizza", (0, split)), ("burger", (split, im.width))):
    part = im.crop((box[0], 0, box[1], im.height))
    part = part.crop(part.getbbox())
    part.save(OUT / "g4" / "assets" / f"g4-{name}.png")
    part.save(ASSET / f"price-card-{name}-transparent.png")
    print(name, part.size)

# ---------- types of inheritance ----------
shutil.copy2(SRC / "3.webp", ASSET / "types-of-inheritance-single-multiple-multilevel.webp")
rgb = np.array(Image.open(SRC / "3.webp").convert("RGB")).astype(np.int16)
H, W = rgb.shape[:2]
mx, mn = rgb.max(axis=2), rgb.min(axis=2)
grey = (mx - mn < 18) & (mn > 70)           # checkerboard (also where the art's shadow darkens it)
lab, _ = ndimage.label(grey)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(border))
bg = ndimage.binary_opening(bg, iterations=1)
alpha = np.where(bg, 0, 255).astype(np.uint8)
# soften the 1-px rim so edges do not show checker fringe
edge = ndimage.binary_dilation(bg, iterations=1) & ~bg
alpha[edge] = 120
rgba = np.dstack([rgb.astype(np.uint8), alpha])
full = Image.fromarray(rgba, "RGBA")
full.save(ASSET / "types-of-inheritance-transparent.png")
full.save(OUT / "g8" / "assets" / "g8-types.png")

# text = cream letters (and their soft shadow) on the orange bars / hub
r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
cream = (r > 200) & (g > 185) & (b > 160) & ~bg
boxes = {  # generous label regions (x0, y0, x1, y1) in source pixels
    "title": (110, 350, 545, 545),
    "single": (890, 120, 1670, 230),
    "multiple": (925, 390, 1680, 500),
    "multilevel": (895, 665, 1670, 775),
}
plate = rgb.copy()
info = {"size": [W, H], "labels": {}}
for key, (x0, y0, x1, y1) in boxes.items():
    m = cream[y0:y1, x0:x1]
    ys, xs = np.where(m)
    bx0, bx1 = x0 + xs.min() - 6, x0 + xs.max() + 7
    by0, by1 = y0 + ys.min() - 6, y0 + ys.max() + 9      # include the drop shadow below
    # clean plate: Telea-inpaint a padded box around the letters + drop shadow, keeping the dark outlines
    mask = np.zeros((H, W), np.uint8)
    px0, py0, px1, py1 = bx0 - (12 if key == 'title' else 2), by0 - 10, bx1 + 14, by1 + 16
    blk = rgb[py0:py1, px0:px1]
    keep = ~((blk[..., 2] > blk[..., 0] + 10) | (blk.max(axis=2) < 45))   # inpaint all but the navy outlines
    mask[py0:py1, px0:px1] = keep * 255
    if key == "title":   # stay inside the hub's inner ring (centre 328,459, inner radius ~215)
        yy, xx = np.mgrid[0:H, 0:W]
        mask[(xx - 328) ** 2 + (yy - 459) ** 2 > 203 ** 2] = 0
    if key == "title":
        plate = cv2.inpaint(plate.astype(np.uint8), mask, 15, cv2.INPAINT_TELEA).astype(np.int16)
    else:   # bars shade only vertically: fill each masked row with that row's colour just right of the label
        for y in range(py0, py1):
            ref = np.median(rgb[y, px1 + 2:px1 + 22], axis=0)
            if ref[0] < 200: continue          # the sample hit the bar's edge (cap curve): leave the row
            row = mask[y, px0:px1] > 0
            plate[y, px0:px1][row] = ref
    # letter cuts: columns with no cream pixels inside the box
    colhit = cream[by0:by1, bx0:bx1].any(axis=0)
    cuts, inside = [], False
    for i, h in enumerate(colhit):
        if h and not inside:
            cuts.append(i); inside = True
        elif not h and inside:
            inside = False
    info["labels"][key] = {"box": [int(bx0), int(by0), int(bx1), int(by1)], "starts": [int(c) for c in cuts]}
    print(key, (bx0, by0, bx1, by1), len(cuts), "letter groups")
plate_img = Image.fromarray(np.dstack([plate.astype(np.uint8), alpha]), "RGBA")
plate_img.save(OUT / "g8" / "assets" / "g8-types-plate.png")
plate_img.save(ASSET / "types-of-inheritance-plate-no-labels.png")
(OUT / "g8" / "assets" / "g8-types-text.json").write_text(json.dumps(info, indent=1))
print("done")

# ---------- per-line letter segments for the type-on (title split into its two lines) ----------
def segs(x0, y0, x1, y1):
    hit = cream[y0:y1, x0:x1].any(axis=0)
    out, s = [], None
    for i, h in enumerate(list(hit) + [False]):
        if h and s is None: s = i
        if not h and s is not None:
            out.append([x0 + s, x0 + i]); s = None
    # merge slivers (< 6 px) into the previous letter
    merged = []
    for a_, b_ in out:
        if merged and (b_ - a_ < 6 or a_ - merged[-1][1] < 1): merged[-1][1] = b_
        else: merged.append([a_, b_])
    # each letter's reveal box runs to the next letter's start (covers the shadow)
    return [[int(m[0]) - 4, int(merged[i + 1][0]) - 4 if i + 1 < len(merged) else int(m[1]) + 10] for i, m in enumerate(merged)]

lines = []
tb = info["labels"]["title"]["box"]
rows = cream[tb[1]:tb[3], tb[0]:tb[2]].any(axis=1)
gap = [i for i in range(len(rows) // 3, 2 * len(rows) // 3) if not rows[i]]
mid = tb[1] + (gap[len(gap) // 2] if gap else len(rows) // 2)
for key, (x0, y0, x1, y1) in [("title1", (tb[0], tb[1], tb[2], mid)), ("title2", (tb[0], mid, tb[2], tb[3]))] + \
        [(k_, tuple(info["labels"][k_]["box"])) for k_ in ("single", "multiple", "multilevel")]:
    sg = segs(x0, y0, x1, y1)
    lines.append({"key": key, "y0": int(y0), "y1": int(y1), "segs": sg})
    print(key, len(sg), "letters")
(OUT / "g8" / "assets" / "g8-types-text.json").write_text(json.dumps({"size": [W, H], "lines": lines}))
