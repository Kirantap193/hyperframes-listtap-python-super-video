# super() in Python — TAP Academy lesson video (HyperFrames)

An animated rebuild of the TAP Academy lecture "super() in Python" (61 storyboard scenes, 45:42 of
lecture → a 7:26 video), made with [HyperFrames](https://hyperframes.heygen.com) (HTML + GSAP).
1920×1080, 30 fps, no audio.

## Preview it

Needs Node.js 18+ and Google Chrome.

```bash
npx --yes hyperframes@0.8.58 preview --port 3015
```

Then open `http://127.0.0.1:3015/#project/<folder-name>` (the Studio shows the timeline and every section).

On Windows, if the bundled headless Chrome is blocked, point HyperFrames at the installed Chrome first:

```bash
export HYPERFRAMES_BROWSER_PATH="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
```

Render (only after the preview is approved):

```bash
npx --yes hyperframes@0.8.58 render --quality delivery -o renders/python-super.mp4
```

## Sections

| Start | Scenes | Composition | Content |
|---|---|---|---|
| 0:00.0 | S03–S09 | `g1-a` | Example 1 typed: Customer, PlatinumCustomer (repeated assignments), display(), main(), dict output |
| 1:02.9 | S10–S13 | `g2-a` | Duplicated lines deleted, `super().__init__(name,phone,email)` typed, same output |
| 1:24.1 | S14–S20 | `g3-a` | Stack / Private Heap trace of constructor chaining |
| 2:20.7 | S21–S24 | `g4-a` | Example 2 Customer with `place_order`; pizza 500 / burger 250 |
| 2:58.8 | S25–S30 | `g5-a` | PlatinumCustomer overrides `place_order`: `return (super().place_order(dish) - delivery_charge)*0.95` |
| 3:50.5 | S31–S34 | `g6-a` | Memory trace of building the object |
| 4:54.7 | S35–S37 | `g7-a` | Memory trace of `place_order('pizza')`: 550 → 475.0 |
| 5:26.6 | S38–S43 | `g8-a` | `RuntimeError: super(): no arguments`, the fix, 475.0, three types of inheritance |
| 5:59.8 | S44–S54 | `g9-a` | Multilevel A ← B ← C with `super(C,self)` / `super(B,self)` |
| 6:42.9 | S55–S61 | `g10-a` | Multiple inheritance C(A,B): `help()` MRO, output A C |

## What is in here

| Path | What it is |
|---|---|
| `index.html` | The master timeline: mounts the ten section compositions back to back |
| `compositions/` | One HTML composition per section (`g1-a` … `g10-a`) |
| `kit-src/` | The shared animation kit (`kit.js`, `kit.css`), `build.py` (bundles it into `assets/kit.js`) and `merge.py` (stitches parallel-built parts into `index.html`) |
| `assets/` | Window art, glossy frames and arrow, Stack / Private Heap panels, and the TAP Academy artwork (`inh-*`) |
| `STYLE-GUIDE.md` | **The animation style for the team** — every look rule, the memory-diagram layout and the kit API |
| `BUILD-BRIEF.md` | The brief each section builder followed for this video |

## How a new lesson video is made with this kit

1. Copy this project, keep `kit-src/` and `assets/`, clear `compositions/` and the mounts in `index.html`.
2. Split the storyboard into ~8–10 groups of scenes; write a `BUILD-BRIEF.md` from this one.
3. Build each group as its own small HyperFrames project (`<video>-parts/gN`), check + snapshot it.
4. `python kit-src/merge.py` to stitch the groups, `npx hyperframes check`, preview, get approval, render.
