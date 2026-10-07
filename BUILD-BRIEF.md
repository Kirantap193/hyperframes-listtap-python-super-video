# video-15 — "super() in Python" — build brief for scene builders

You build ONE group of scenes of a HyperFrames lesson video (1920x1080, 30 fps, no audio) that
re-makes the user's storyboard as a premium animated lesson on a black stage. **The user approved
the final look of video-12 (Encapsulation) and video-13 (Inheritance) after many rounds of
corrections. This video must look exactly like that final state from the very first preview.
Every rule below was a correction — breaking one is a regression.**

Read before writing (finished compositions in the approved style):
- `C:\Users\kiran\Documents\hyperframes\video-13\compositions\g5-a.html`, `g7-a.html` (code typing,
  output, editor scrolling — `scroll()` helper in g7-a), `g1-b.html` (the user's artwork revealed
  piece by piece incl. the three-types-of-inheritance art `types3.png`), and
  `video-12\compositions\g4-a.html`, `g5-a.html`.
- Memory-diagram groups (g3, g6, g7, g8) ALSO read: `C:\Users\kiran\Documents\hyperframes\video-template\STYLE.md`
  and `C:\Users\kiran\Documents\hyperframes\video-5-part2\compositions\citizen-memory.html`
  (+ `citizen-memory2/4.html`) — the approved Stack / Private Heap look (frames push, `__new__`
  with cls + `*args` tuple cells, heap object cards, addresses fly heap → stack, values fly
  stack → heap, arrows drawn on). Adapt them to the rules below (no glow, no bold).
- Full kit source: `C:\Users\kiran\Documents\hyperframes\video-15\kit-src\kit.js` (+ kit.css).

## Storyboard (source of truth for content)

- `C:\Users\kiran\OneDrive\Desktop\StoryBoard\Storyboards\Super\context.md` — §1 lesson arc,
  §3 final code, §5 one section per scene (`### S15 …`): animation order, **Final on-screen
  state** (copy code / output character for character, but see "Names"), narration (tells you
  what is taught and in which order).
- Frames: `...\Storyboards\Super\frames\SNN_final.jpg`, `SNN_stepK.jpg` — LOOK at them.
- Follow the storyboard's teaching flow and its own diagrams (memory traces, types list, pizza /
  burger prices). **Do not add visuals that are not in the storyboard** (no extra icons,
  characters, illustrations, decorative shapes).
- Ignore: presenter, logos, intro stings, the "super()" title label, the matrix-rain monitor (output
  goes in OUR output window), Spyder chrome (autocomplete popups, bracket-match boxes, selections,
  occurrence highlights, cursors, scroll jitter), `C:\Users\Studio\.spyder-py3>python temp.py` /
  `cls` prompt lines, typos/backspaces (type the final text once), title cards.

## NEVER (each of these was a user correction)

- No section headings, no title cards, no summary cards, **no explanation/note/caption boxes that
  explain code in words** (do not use `k.note`, `k.cap`, `k.header`). Code, output and diagrams
  carry the lesson; the trainer explains in class.
- **No glow** anywhere (no `0 0 Npx` box-shadow / drop-shadow halos — this includes the memory
  style's arrow glow and red dashed highlight glow: drop them). Depth = stacked hard edges + soft
  drop shadow below.
- **No bold** anywhere (font-weight 400 everywhere, also Stack/Heap labels and card text). Bigger text instead.
- No pointer/chevron marks, no shake/bump/pulse/elastic wobble (settle with `power2.out`/
  `power3.out`), no effect on the code window before output appears. No "pointed_at" emphasis —
  the storyboard's presenter gestures become nothing (or a short pause).
- **No code or output highlighting**, except the kit's automatic neon-yellow bar on a line that
  is edited/inserted INSIDE existing code (free via `cw.edit` and inserted lines). No red dashed
  highlight boxes on heap lines either.
- No boxes that repeat what the output window already shows.
- Never wrap a code line. A printed line never wraps — exceptions: the instance `__dict__` print
  wraps one entry per line (see below), and `help(...)` output is shown as Python's lines.
- No dead time: anything > 2 s without visible change is auto-trimmed by the kit to 1 s, so don't
  pad with long holds — but DO keep the short teaching pauses (they become PPT click points).

## Names: full variable names (user rule)

`p` → `platinum_customer`, `ph` → `phone`, `addr` → `address`, `ph_no` → `phone_no`,
`del_charge` → `delivery_charge`, `plat_id` → `platinum_id`, `c` → `c_object`.
Class name `PlatiniumCustomer` → **`PlatinumCustomer`** (correct spelling) everywhere — code,
memory cards, cls cell. Class names `Customer`, `A`, `B`, `C`, `object` and method names
`display`, `place_order`, `fun`, `test`, `main` stay. Keep the storyboard's spacing (e.g.
`(self,name,phone,email)` without spaces after commas where the storyboard has none). Output
strings exactly as Python would print them with these names.

## The code (final states, with full names)

Example 1 (g1–g3). The constructor call is split over two lines **from the start** (the storyboard
does this from S14; it keeps the code window ≈ 1000 px wide so the output fits beside it):
```python
class Customer:

    def __init__(self,name,phone,email):
        self.name = name
        self.phone = phone
        self.email = email


class PlatinumCustomer(Customer):

    def __init__(self,name,phone,email,platinum_id):
        super().__init__(name,phone,email)          # g1: the three duplicated assignments
        self.platinum_id = platinum_id               #     self.name/phone/email = ... instead

    def display(self):
        print(self.__dict__)

def main():
    platinum_customer = PlatinumCustomer(
        'Rohit', 9900887766,'rohit@gmail.com', 10)
    platinum_customer.display()

if __name__ == '__main__':
    main()
```
Output (the dict wraps one entry per line — allowed):
```
{'name': 'Rohit',
 'phone': 9900887766,
 'email': 'rohit@gmail.com',
 'platinum_id': 10}
```
Example 2 (g4–g8):
```python
class Customer:

    def __init__(self,name,address,phone_no):
        self.name = name
        self.address = address
        self.phone_no = phone_no

    def place_order(self,dish):
        cost = 0
        delivery_charge = 50
        if dish == 'pizza':
            cost = 500 + delivery_charge
        else:
            cost = 250 + delivery_charge
        return cost

class PlatinumCustomer(Customer):

    def __init__(self,name,address,phone_no,platinum_id):
        super().__init__(name,address,phone_no)
        self.platinum_id = platinum_id

    def place_order(self,dish):
        delivery_charge = 50
        return (super().place_order(dish) - delivery_charge)*0.95


def main():
    platinum_customer = PlatinumCustomer(
        'Rohit', 'ITC', 9900887766, 12)
    print(platinum_customer.place_order('pizza'))

if __name__ == '__main__':
    main()
```
Output `475.0`. The broken version (g7 → g8) has the return line split by an Enter:
`        return` / `        (super().place_order(dish) - delivery_charge)*0.95` → error output
shows ONLY the last traceback line in red: `RuntimeError: super(): no arguments`.

Example 3 (g9) and Example 4 (g10): §3 of context.md with `c` → `c_object`
(`c_object = C()`, `c_object.fun()`, `help(c_object)`, `c_object.test()`).

The code is taller than the screen: when it no longer fits (content area y 150 → 1040, minus the
title bar), scroll the editor like video-13 `g7-a.html` (top lines leave, the rest slides up) or
fold a finished class body to its header line as the storyboard does — never shrink the font
(except the memory layout below).

## Look (implemented by the kit — use it, don't restyle it)

- Black stage `#010101`. The kit lifts every scene 56 px (no heading band), so author in the old
  coordinates: content area y 150 → 1040, x 64 → 1856.
- **Code window**: `k.win({x:64, y:150, w:900, h:400, title:"Main.py", dash:true, font:30, lh:43})`
  — **font 30 / lh 43 in every non-memory beat**. The user's video-7 window, PyCharm-derived
  colours. It **auto-sizes**: width hugs its longest line, height follows the visible lines.
- **Output window**: `k.win({x:1000, y:150, w:856, h:200, title:"output", out:true, font:30, lh:43})`
  — sits at the TOP level with the code window; the kit pushes it ≥ 50 px clear of the code window
  and sizes it to exactly the printed lines. Print with `ow.print(text, cls, t)`; `"o-err"` for the
  red error line, `ow.clear(t)` to clear. Never overlapping anything.
- **Boxes**: `k.chip({x, y, w, main, sub, color})` = the user's glossy 3-D frame (violet, pink,
  teal, blue, orange, green, amber, red) with white normal-weight lettering (42 px main / 28 px sub).
- **Arrows**: `k.arrow({d:"M x y H x2"})` straight horizontal = the user's glossy arrow image; any
  other path = smooth solid sky-blue #4fd1ff 3-D arrow (no glow). Start exactly at the source, never
  cross boxes or text; draw arrows that pass over windows on a top layer
  (`var TOP = k.layer({x:0,y:0,w:1920,h:1080})` created after the windows).

## Memory layout (g3, g6, g7, g8 — MUST be identical across groups)

Authoring coordinates (before the kit's 56 px lift):
- **Code window (memory beats)**: `k.win({x:36, y:150, w:600, h:400, title:"Main.py", dash:true, font:16, lh:24})`
  — the same window style at the memory size (16 / 24). Enter it from the font-30 window with a
  smooth dissolve/glide (storyboard S14/S31: "code shrunk for memory analysis"). Its right edge
  must stay ≥ 40 px left of the Stack frame names.
- **Stack panel**: `mem-stack2.png` nine-slice (`border-image: url(assets/mem-stack2.png) 120 fill / 50px`),
  left 1010, top 150, width 440, height 810. **Private Heap**: `mem-heap2.png`, left 1478, top 150,
  width 408, height 810. Labels **under** the panels (top 975), white Nunito **400**, 38 px:
  `Stack`, `Private Heap`. Both pop in with a 3-D flip (rotationY / transformPerspective).
- **Frames**: SVG dashed rounded rects (stroke `#c8d6ff` @ 0.45, width 2.5, dash 7 6, fill
  rgba(255,255,255,0.03), radius 20), 400 wide at left 1030, stacked bottom-up from the panel
  bottom (`main()` at the bottom). Push = drop in from above (y −360 → 0, power3.out); pop =
  lift + fade out. Frame names outside the Stack, right-aligned to x 996, JetBrains Mono 400 17 px
  `#8d96ab`; `__new__` writes its name on two lines (`__new__` / `(cls,*args,**kwargs)`).
- **Stack text**: labels white 20 px (`self`, `*args`, `cls` pink `#ffb0c2`), values in boxes
  (`#0b1836`, 1.5 px `#3b5ea8`, radius 8) 18–20 px; the `*args` tuple = index digits `#c9d2e8`
  over cells; if four cells do not fit in one row, use two rows of cells.
- **Heap object** = card 340 wide at left 1512: teal header (`#127a68` → `#0c5c50`) holding the
  address `1000` (white 24 px) and a class tag `PlatinumCustomer`; body `#0e1a28` with lines
  `name = 'Rohit'` (key `#9fb4cc`, `=` and value white, 18–19 px). No Key/Value tables, no "dict" label.
- **Motion**: frames push one by one; addresses **fly heap → stack** (a copy of `1000` glides from
  the card header into the `self` / variable box); values **fly stack → heap** (copy glides from the
  stack box into the card line — never typed); reference arrows = sky-blue curved `k.arrow` from the
  stack box to the card header, drawn on (`k.draw`), no glow. When a method returns, its frame pops
  (fade + lift) and its arrows undraw. Returned values (e.g. `550`) fly from the returning frame
  into the waiting expression's frame.
- **Output during memory beats**: the memory (Stack + Heap + arrows) fades out, the output window
  pops at the top right (level with the code window, ≥ 50 px clear), prints, fades, and the memory
  fades back in with its full state.

## Code typing rules (trainer pacing — the PPT is cut at the pauses)

- Code the viewer has not seen yet is **typed**, never shown whole: `cw.typeCode(lines, t)` for
  blocks (≈0.5 s before every line, ≈1 s after a `class`/`def` header). Single lines:
  `cw.type(line, t)`. Assignments type value first automatically. Code already seen in an earlier
  group appears at the start of your group via `cw.show(lines, t)` (fast) — then type only what is new.
- Inserting a line inside existing code: `cw.moveTo` the lines below down one row (same instant),
  then `cw.add` + `cw.type` the new line (kit auto-highlights it). Editing a line in place:
  `var L2 = cw.edit(L, "new text", t); t = L2.t;` (auto-highlight). Deleting lines: `cw.fade` them,
  then `cw.moveTo` the lines below up (close the gap).
- After the code that produces output: pause ~0.6 s, `ow.pop`, then print (no effect on the code
  window). Clear the output (`ow.clear`) before a new run.

## Make it MORE aesthetic and MORE animated — within the rules

3-D motion (rotationX/Y flips with `transformPerspective`, depth glides on `z`), diagrams assembling
piece by piece, smooth power3.out settles, short pauses after each step. Seek-safe only
(`k.move` = fromTo with immediateRender:false). Fill the frame: code left, everything else right,
nothing cut off, nothing overlapping, text large.

## Kit API (shared kit — `assets/kit.js`, do not edit)

```js
var k = K.make(root, tl);
var cw = k.win({x:64, y:150, w:900, h:400, title:"Main.py", dash:true, font:30, lh:43});
var L = cw.block(["class A:", "", "    def fun(self):", "        print('A')"], 0); // "" = half-row blank; blanks not in L
t = cw.pop(t);  t = cw.typeCode(L, t);  t = cw.type(line, t);  t = cw.show(lines, t);
var L2 = cw.edit(L[1], "    def test(self):", t); t = L2.t;   cw.fade(line, t);  cw.moveTo(line, row, t);
var ow = k.win({x:1000, y:150, w:856, h:200, title:"output", out:true, font:30, lh:43});
t = ow.pop(t); t = ow.print("475.0", "", t); ow.print("RuntimeError: super(): no arguments", "o-err", t); t = ow.clear(t);
var c = k.chip({x, y, w:300, main:"pizza", sub:"500", color:"orange"});
var a = k.arrow({d:"M1200 600 C 1250 500 1300 500 1350 450"});  t = k.draw(a, t, 0.6);  k.undraw(a, t);
k.pop(el,t) k.land(el,t) k.rise(el,t) k.fade(el,t) k.wipe(el,t) k.out(els,t,dur) k.move(el, from, to, t, dur, ease)
k.el(tag, cls, cssText, html, parent) / k.hide(el)   // raw elements (hidden until animated)
var Ly = k.layer({x,y,w,h});  Ly.arrow / Ly.draw / Ly.chip ...
```

## Composition file shape (copy exactly; prefix every id/class with your group prefix)

```html
<template id="g2-a-template">
  <style> #root { position: absolute; inset: 0; overflow: hidden; pointer-events: none; } </style>
  <div id="root" data-composition-id="g2-a" data-width="1920" data-height="1080" data-duration="NN"></div>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script src="assets/kit.js"></script>
  <script>
    (function () {
      var tl = gsap.timeline({ paused: true });
      var root = document.querySelector('[data-composition-id="g2-a"]');
      var k = K.make(root, tl);
      ... build ...
      window.__timelines["g2-a"] = tl;
    })();
  </script>
</template>
```
- Your part project is `C:\Users\kiran\Documents\hyperframes\video-15-parts\gN\` (assets + kit.js
  already there; `index.html` mounts `compositions/gN-a.html`). ≤ 300 lines outside `<style>` per
  file (lint); split by time into `gN-a`, `gN-b`, … if needed (add each mount to your index.html,
  back to back, alternating `data-track-index` 0/1; the next file starts from the previous one's
  exact end state). Set `data-duration` (file AND index.html mount AND the index root) to your
  timeline end. Do NOT touch any other group's folder, video-15 itself, or video-12/13/14.
- Seek-safe only (no Date.now / Math.random / fetch). Unique ids/classes with your prefix.
- Your group **starts on black and ends with everything faded out** (~0.6 s fade at the end).
- New images (only if the storyboard needs them): put them in your `assets/` with your group prefix.

## Check + look (required)

Bash with `dangerouslyDisableSandbox: true`, from your part folder:
```bash
export HYPERFRAMES_BROWSER_PATH="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
npx --yes hyperframes@0.8.58 check            # 0 errors (ignore the "pins 0.8.58" notice — do NOT upgrade)
npx --yes hyperframes@0.8.58 snapshot --at 5,12,20 --no-end --describe false -o snaps
```
Snapshot EVERY key beat and LOOK at the images: nothing overlaps (code vs output vs diagram vs
frame names), nothing cut off, no glow, no bold, no text boxes, arrows land on targets, code typed
in order, output exact. Fix, re-snapshot, then delete `snaps`.
Python: `C:\Users\kiran\AppData\Local\Programs\Python\Python312\python.exe`. Write patch scripts with
the Write tool (bash heredoc quoting breaks on Windows).

Report back (short): file names, composition ids + durations, a one-line beat list with times, and
anything you could not replicate.
