"""S42 Types of Inheritance from the user's PARTS sheet (clean transparency, smooth edges).

Writes into video-15-parts/g8/assets:
  g8p-hub.png / g8p-hub-plate.png      circle with / without its title
  g8p-bar{1,2,3}.png / -plate.png      bars with / without their label
  g8p-text.json                         sizes + per-letter segments for the type-on
"""
import json, pathlib
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = pathlib.Path(r"C:\Users\kiran\OneDrive\Asset's\Super\types-of-inheritance-parts-sheet.webp")
OUT = pathlib.Path(r"C:\Users\kiran\Documents\hyperframes\video-15-parts\g8\assets")
sheet = np.array(Image.open(SRC).convert("RGBA"))
BOX = {"hub": (84, 30, 630, 561), "bar1": (688, 18, 1675, 201), "bar2": (688, 221, 1675, 405), "bar3": (688, 420, 1675, 605)}


def letters(cream, x0, y0, x1, y1):
    hit = cream[y0:y1, x0:x1].any(axis=0)
    runs, s = [], None
    for i, h in enumerate(list(hit) + [False]):
        if h and s is None: s = i
        if not h and s is not None: runs.append([x0 + s, x0 + i]); s = None
    m = []
    for a, b in runs:
        if m and (b - a < 6): m[-1][1] = b
        else: m.append([a, b])
    return [[max(0, a - 4), (m[i + 1][0] - 4) if i + 1 < len(m) else b + 10] for i, (a, b) in enumerate(m)]


info = {}
for name, (x0, y0, x1, y1) in BOX.items():
    im = sheet[y0:y1, x0:x1].copy()
    lab, _ = ndimage.label(im[..., 3] > 20)                # keep only this part (no neighbouring pieces)
    ids, cnt = np.unique(lab[lab > 0], return_counts=True)
    im[lab != ids[np.argmax(cnt)]] = 0
    H, W = im.shape[:2]
    rgb = im[..., :3].astype(np.int16)
    a = im[..., 3]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    cream = (r > 200) & (g > 185) & (b > 160) & (a > 200)
    if name != "hub":
        hitc = cream.any(axis=0)                           # the number badge is not label text:
        cut = next(x for x in range(150, W) if not hitc[x])  # first empty column after the badge
        cream[:, :cut] = False
    ys, xs = np.where(cream)
    bx0, bx1, by0, by1 = xs.min() - 6, xs.max() + 7, ys.min() - 6, ys.max() + 9
    plate = rgb.copy()
    if name == "hub":
        # inner disk = everything inside the dark inner ring; replace it by a smooth cubic fit
        dark = rgb.max(axis=2) < 70
        cy, cx = H // 2, W // 2
        row = np.where(dark[cy])[0]; col = np.where(dark[:, cx])[0]
        left = row[row < cx].max(); right = row[row > cx].min()
        top = col[col < cy].max(); bot = col[col > cy].min()
        ccx, ccy = (left + right) / 2, (top + bot) / 2
        rad = min(right - left, bot - top) / 2 - 3
        yy, xx = np.mgrid[0:H, 0:W]
        r2 = (xx - ccx) ** 2 + (yy - ccy) ** 2
        txt = ndimage.binary_dilation(cream, iterations=14); txt = txt | np.roll(txt, 9, axis=0)
        fitm = (r2 < (rad - 6) ** 2) & ~txt
        X = np.stack([np.ones_like(xx), xx / 1e3, yy / 1e3, xx * xx / 1e6, xx * yy / 1e6, yy * yy / 1e6,
                      xx ** 3 / 1e9, xx * xx * yy / 1e9, xx * yy * yy / 1e9, yy ** 3 / 1e9], -1).astype(float)
        w = np.clip((rad - np.sqrt(r2)) / 4.0, 0, 1)
        for c in range(3):
            coef, *_ = np.linalg.lstsq(X[fitm], rgb[..., c][fitm].astype(float), rcond=None)
            plate[..., c] = (rgb[..., c] * (1 - w) + np.clip(X @ coef, 0, 255) * w).astype(np.int16)
        rows = cream[by0:by1].any(axis=1)
        gap = [i for i in range(len(rows) // 3, 2 * len(rows) // 3) if not rows[i]]
        mid = by0 + (gap[len(gap) // 2] if gap else len(rows) // 2)
        lines = [{"y0": int(by0), "y1": int(mid), "segs": letters(cream, bx0, by0, bx1, mid)},
                 {"y0": int(mid), "y1": int(by1), "segs": letters(cream, bx0, mid, bx1, by1)}]
        info[name] = {"size": [W, H], "lines": lines, "centre": [float(ccx), float(ccy)]}
    else:
        # erase letters + shadow: per row, anything far from the row's clean orange becomes that orange
        m = ndimage.binary_dilation(cream, iterations=6); m = m | np.roll(m, 8, axis=0)
        py0, py1 = by0 - 10, min(H - 1, by1 + 14)
        xa, xb = bx0 - 6, min(W - 1, bx1 + 10)
        for y in range(py0, py1):
            seg = rgb[y, xa:xb]; mm = m[y, xa:xb].copy()
            ok = ~mm & (seg[:, 0] > 200) & (seg[:, 1] < 150)
            if ok.sum() < 20: continue
            med = np.median(seg[ok], axis=0)
            far = np.abs(seg - med).sum(axis=1) > 40
            mm |= far & (seg[:, 0] > 120)               # leave the dark outline alone
            plate[y, xa:xb][mm] = med
        # soften what is left horizontally only (keeps the bar's top-to-bottom shading)
        reg = plate[py0:py1, xa + 4:xb - 4].astype(float)
        plate[py0:py1, xa + 4:xb - 4] = ndimage.gaussian_filter1d(reg, 10, axis=1).astype(np.int16)
        info[name] = {"size": [W, H], "lines": [{"y0": int(by0), "y1": int(by1), "segs": letters(cream, bx0, by0, bx1, by1)}]}
    Image.fromarray(im, "RGBA").save(OUT / f"g8p-{name}.png", optimize=True)
    Image.fromarray(np.dstack([plate.astype(np.uint8), a]), "RGBA").save(OUT / f"g8p-{name}-plate.png", optimize=True)
    print(name, (W, H), [len(l["segs"]) for l in info[name]["lines"]])
(OUT / "g8p-text.json").write_text(json.dumps(info, default=int))
