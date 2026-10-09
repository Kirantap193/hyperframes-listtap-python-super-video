"""super() title art (2026-10-09) -> g0 intro: the art without the word (plate) + per-letter crops for the type-on."""
import json, pathlib
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = pathlib.Path(r"C:\Users\kiran\OneDrive\Asset's\Super\super-title.webp")
OUT = pathlib.Path(r"C:\Users\kiran\Documents\hyperframes\video-15-parts\g0\assets")
OUT.mkdir(parents=True, exist_ok=True)
im = np.array(Image.open(SRC).convert("RGBA"))
H, W = im.shape[:2]
rgb = im[..., :3].astype(np.int16)
X0, X1, Y0, Y1 = 640, 1915, 212, 552                     # the word "super()" on the dark panel
plate = rgb.copy()
# the panel is smooth: per row, interpolate its colour between a strip left of the word and one right of it
xs = np.arange(X0, X1)
txt = np.zeros((H, W), bool)
for y in range(Y0, Y1):
    L = np.median(rgb[y, 612:640], axis=0); R = np.median(rgb[y, 1884:1912], axis=0)
    f = ((xs - 626) / (1898 - 626))[:, None]
    base = L * (1 - f) + R * f
    d = np.abs(rgb[y, X0:X1] - base).sum(axis=1)
    txt[y, X0:X1] = d > 12
    plate[y, X0:X1] = base.astype(np.int16)                # the whole strip becomes clean panel
txt = ndimage.binary_opening(txt, iterations=1)
# keep the panel's own texture outside the word: only replace pixels near the word
keepm = ~ndimage.binary_dilation(txt, iterations=10)
plate[keepm] = rgb[keepm]
# letters: column runs of word pixels
face = (rgb.min(axis=2) > 200)
hit = face[Y0:Y1, X0:X1].any(axis=0)
runs, s = [], None
for i, h in enumerate(list(hit) + [False]):
    if h and s is None: s = i
    if not h and s is not None: runs.append([X0 + s, X0 + i]); s = None
runs = [r for r in runs if r[1] - r[0] > 8]
segs = [[r[0] - 6, (runs[i + 1][0] - 6) if i + 1 < len(runs) else r[1] + 14] for i, r in enumerate(runs)]
Image.fromarray(im, "RGBA").save(OUT / "g0-title.png", optimize=True)
Image.fromarray(np.dstack([plate.astype(np.uint8), im[..., 3]]), "RGBA").save(OUT / "g0-title-plate.png", optimize=True)
(OUT / "g0-title.json").write_text(json.dumps({"size": [W, H], "y0": Y0, "y1": Y1, "segs": segs}, default=int))
print(len(segs), "letters", segs)
