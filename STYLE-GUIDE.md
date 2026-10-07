# TAP Academy lesson-video animation style

The approved look for TAP Academy Python lesson videos, built with HyperFrames + the shared kit in
`kit-src/`. Every rule here came from a reviewer correction on earlier videos (Encapsulation,
Inheritance, Methods of Inheritance, super()). Build to all of it from the first preview.

## 1. Never

- Section headings, intro / title / summary cards, explanation / note / caption boxes. Code, output
  and diagrams carry the lesson; the trainer explains in class.
- Glow of any kind (no `0 0 Npx` halos). Depth = stacked hard edges + a soft drop shadow below.
- Bold text. Everything is font-weight 400; make text bigger instead.
- Pointer marks; shake, bump, pulse or elastic wobble. Settle with `power2.out` / `power3.out`.
- Any effect on the code window before output appears.
- Highlighting code or output. The one exception: a neon-yellow bar (`#eaff00`, tint .24, 6 px left
  bar) on a line that is being edited or inserted inside existing code (the kit adds it).
- Boxes that repeat what the output window already shows.
- Dead time: anything > 2 s with no visible change is trimmed to a 1 s pause (the kit does this).
- Rendering before the local Studio preview is approved.

## 2. Stage and layout

- 1920×1080, 30 fps, flat black `#010101`.
- Code on the left, everything else on the right, nothing overlapping, fill the frame.

## 3. Code window

- The Main.py window: title-bar art (`assets/code-titlebar.webp`), flat `#101b2c` body, `#26344b`
  inner panel, thin white dashed outline.
- Font 30 / line height 43 in every scene (memory-trace scenes use 16 / 24, see §6).
- Colours (PyCharm-derived): plain `#ffffff`, keywords `#c099ff`, numbers `#f5a97f`, strings
  `#e0c78b` italic, builtins / `def` and `class` names `#8fb3ff`, `self` `#d48fcf`, decorators
  `#e3d55a`, comments grey.
- The window hugs its longest line; its height grows and shrinks with the visible lines.
- Code is **typed**, never shown whole the first time: ~0.5 s pause before every line, ~1 s after a
  `class` / `def` header before the body. Adding a line inside a method: step inside, pause, type.
  Assignments type the value first, then `=`, then the name.
- When the code is taller than the screen, the editor scrolls (top lines leave, the rest slides up)
  or a finished class body folds — the font never shrinks.

## 4. Output window

- Output-titlebar art (`assets/output-titlebar.webp`), `#0c1620` body, white text; errors `#ff6b6b`,
  showing only the last traceback line.
- Only the real printed lines. Top-aligned with the code window, ≥ 50 px clear of it, sized to
  exactly the printed lines.
- A printed line never wraps (a long instance `__dict__` may wrap one entry per line).

## 5. Boxes, arrows, artwork

- Boxes = the glossy frames (`gl-frame-violet.png`, `gl-frame-pink.png`, nine-sliced, hue-rotated
  per colour) with white normal-weight lettering ~42 px. Text inside a box is typed after the box lands.
- Straight box-to-box arrows = the glossy arrow image (`gl-arrow.png`). Curved arrows = smooth solid
  sky-blue `#4fd1ff` with 3-D depth (dark under-stroke, bright core), starting exactly at their
  source and never crossing boxes or text.
- The trainer's own artwork is used as-is. When a final image + parts sheet is supplied, build it
  from crops of the final image at exact positions and end pixel-identical (no ghosting cross-fades).
- Follow the storyboard's teaching flow and its own diagrams; add no visuals that are not in it.
- Full variable names everywhere (`platinum_customer`, not `p`; `delivery_charge`, not `del_charge`).

## 6. Stack / Private Heap memory diagrams

- Code window shrinks to font 16 / lh 24 at x 36.
- Stack panel `mem-stack2.png` (left 1010, 440 wide), Private Heap `mem-heap2.png` (left 1478,
  408 wide), both top 150, 810 tall, nine-slice `120 fill / 50px`; labels under the panels, white,
  Nunito 400, 38 px. (Coordinates are authoring coordinates; the kit lifts every scene 56 px.)
- Frames: dashed rounded rects (`#c8d6ff` @ 0.45, 2.5 px, dash 7 6), `main()` at the bottom,
  pushed one by one from above and popped (lift + fade) when the method returns. Frame names sit
  outside the Stack, right-aligned, grey `#8d96ab` 17 px.
- Values sit in dark boxes (`#0b1836`, 1.5 px `#3b5ea8`); `self`, `cls`, `*args` labels pink `#ffb0c2`.
- Heap objects are cards: teal header (`#127a68` → `#0c5c50`) with the address (e.g. `1000`) and a
  class tag, dark body with lines `name = 'Rohit'`. No key/value tables, no "dict" label.
- Addresses fly heap → stack; values fly stack → heap (never typed); reference arrows are sky-blue
  curves drawn on from the stack box to the card header.
- For output, the memory fades out, the output window prints, then the memory fades back in.

## 7. Motion

More aesthetic, more animation — within the rules: 3-D entrances (rotationX / rotationY flips with
`transformPerspective`, depth glides on `z`), diagrams assembling piece by piece, short pauses after
every step (they become the click points of the trainer PowerPoint). Seek-safe only — no
`Date.now`, `Math.random` or network calls.

## 8. Kit API (`assets/kit.js`, source in `kit-src/`)

```js
var k = K.make(root, tl);
var cw = k.win({x:64, y:150, w:900, h:400, title:"Main.py", dash:true, font:30, lh:43});
var L = cw.block(["class A:", "", "    def fun(self):", "        print('A')"], 0);  // "" = half-row blank
t = cw.pop(t);  t = cw.typeCode(L, t);  t = cw.type(line, t);  t = cw.show(lines, t);
var L2 = cw.edit(L[1], "    def test(self):", t); t = L2.t;   cw.fade(line, t);  cw.moveTo(line, row, t);
var ow = k.win({x:1000, y:150, w:856, h:200, title:"output", out:true, font:30, lh:43});
t = ow.pop(t); t = ow.print("475.0", "", t); ow.print("RuntimeError: ...", "o-err", t); t = ow.clear(t);
var c = k.chip({x, y, w:300, main:"pizza", sub:"500", color:"orange"});
var a = k.arrow({d:"M1200 600 C 1250 500 1300 500 1350 450"});  t = k.draw(a, t, 0.6);  k.undraw(a, t);
k.pop / k.land / k.rise / k.fade / k.wipe / k.out / k.move(el, from, to, t, dur, ease) / k.el / k.layer
```

Edit `kit-src/kit.js` / `kit.css`, then run `python kit-src/build.py` to rebuild `assets/kit.js`.

## 9. Delivery

1. Preview in HyperFrames Studio; reviewers send timestamped screenshots; change only what they point at.
2. After approval: `render --quality delivery`, verify with ffprobe, and hash-check copies.
3. Build the click-by-click trainer PowerPoint from the render (one slide per pause).
