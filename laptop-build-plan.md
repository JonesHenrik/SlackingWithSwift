# The laptop on the desk — Build Plan

> Companion to `plan.md` and `build-plan.md`. This is a **standalone phase document**: it is
> deliberately not folded into `build-plan.md` and it renumbers nothing there. Written 2026-08-18.
>
> It inherits, rather than restates, two sections of `build-plan.md`: *The design language —
> "Haunted Glass"* (palette, hard shadow, type, Reduce Motion) and *Phase 0 — The phone in your
> hand*, which is the direct precedent and whose structure this document copies.
>
> **Status:** built, not yet compiled or seen running. All four files exist and are wired
> together; see *Remaining work* at the end, which is the honest state of it.
>
> **Two changes were made after this document was written** and are folded into the text below
> rather than appended: the status line reads `HOLD TO SCROLL`, not `HOLD TO WORK`, and the
> `.turning` alert has **no countdown bar**.

---

## Why

The game's fiction is "slack off while Paul isn't looking." Phase 0 put the *slacking* on screen —
a pixel hand and phone that rise from the bottom-right while you hold. The other half of the
fiction has never been visible: **the work you are supposedly doing**. Today "not holding" is
expressed as grey text on a glass card reading `NOT HOLDING — NO POINTS`.

This adds a pixel-art laptop across the bottom of the screen, permanently present, running a live
Claude Code session in its terminal. Claude does the work while you slack on your phone. That is
the joke, and it is the thing that makes the premise legible to someone watching over your
shoulder — which is exactly the argument Phase 0 made for the phone.

**It is not, however, purely cosmetic, and that is the important difference from Phase 0.**
`plan.md:45` calls the phone "the one purely cosmetic element in the game and it should stay that
way." This layer breaks that: the laptop screen **absorbs the status readout** and the glass status
card is deleted. So the laptop is a game surface, not a prop. Everything downstream in this
document — the alert state, the grayscale test, the accessibility exception — follows from that one
decision.

---

## The shape of it

```
                 [ Paul ]

  ┌──────────────────────────────┐
  │ › fix flaky test             │      not holding: the agent works
  │ ⏺ Read  Engine               │
  │ ⏺ Edit  Curve                │
  │ ✦ Working… 12s               │
  │ ──────────────────────────── │
  │ HOLD TO SCROLL               │
  └──────────────────────────────┘
  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄      keyboard deck


                 [ Paul ]

  ┌──────────────┬───────────────┐
  │  ██   ███    │               │      turning: the terminal is
  │  ██   █      │      ▐███▌    │      interrupted. The phone is up,
  │  ██   ███    │      ▐███▌    │      so the alert lives in the left
  │  ████████    │      ▐███▌    │      half where it can't be covered.
  │ ████▌        │      ▐███▌    │
  └──────────────┴───────────────┘
```

---

## Build

### `Game/MicroFont.swift` — new, and a reuse cleanup

The terminal needs letters. Today the project has a 3×5 **digit** font only — `digitArt` and
`digits(_:into:x:y:width:color:)` at `Game/PhoneScreenSim.swift:285-306`, used for the runner's
score.

- Extend it to a monospace 3×5 set: `A–Z`, `0–9`, and the punctuation the terminal needs —
  `› ⏺ ✦ ✓ + - . , : / _ ' ! ? ( ) # > ×` and space. The marks (`⏺`, `✦`, `✓`) are approximations
  drawn on a 3×5 lattice, not glyph traces.
- **Metrics, fixed:** glyph 3 wide × 5 tall, **4px horizontal pitch** (3 + 1 gutter), **6px line
  pitch** (5 + 1). These match `digits` exactly so the two callers stay in sync.
- A **double-height variant** — 6 × 10, 8px pitch, 12px line pitch — used *only* for the poster word
  in the alert state. Nowhere else.
- **Move `digitArt` and `digits` out of `PhoneScreenSim` into this file** and have the runner call
  through, so the project has one font rather than two. `PixelGrid.stamp(_:x:y:_:)`
  (`PhoneScreenSim.swift:71`) already renders `[String]` art and needs no change — this is a move,
  not a rewrite.

### `Game/LaptopScreenSim.swift` — new

Mirrors `PhoneScreenSim`'s contract exactly. **Pure, no state, no timer** — every frame is a
function of its arguments, so it inherits `PaulGameView`'s existing `TimelineView(.animation)` and
does not violate `plan.md`'s no-tick-loop rule.

```swift
enum LaptopScreenSim {
    static let columns = 70
    static let rows = 30
    static func render(elapsed: Double, seed: UInt64, state: LaptopState) -> PixelGrid
}
```

`LaptopState` is a small value type **the view derives from the engine** — phase, `isHolding`,
`phaseProgress`, and the current stare line. `GameEngine` is not touched and gains no knowledge
that this layer exists.

**Text budget, and it is tight.** The well is 70 × 30 art pixels with 1px padding, so at the
metrics above: **17 characters per line, 4 terminal lines, plus a 1px rule and one status line** —
which consumes rows 1–29 of 30 exactly. There is no slack; a fifth line does not fit.
Every line of copy in this document has been written to fit; new copy must be counted, not
estimated.

```
 row  1   › fix flaky test        16
 row  7   ⏺ Read  Engine          14
 row 13   ⏺ Edit  Curve           13
 row 19   ✦ Working… 12s          14
 row 24   ────────────────────    rule
 row 25   HOLD TO SCROLL          14
```

**Working mode** (`.idle`, `.green`, `.fakeOut`) — the agentic loop. Lines accumulate and scroll
upward out of the top. Use the runner's deterministic spawn idiom verbatim
(`PhoneScreenSim.swift:198-206`): derive `newest` and `oldest` step indices from `elapsed`, replay
that range, store nothing. A seeded task list means each run reads differently. The spinner glyph
cycles and the elapsed counter ticks, so the screen is alive even when no new line has landed.

The **status line** is the bottom row, set in the terminal's own idiom — a TUI status bar, not a
label pasted on. It carries what the glass card carried: `HOLD TO SCROLL`, `EARNING ×2.4`,
`FALSE ALARM`.

`HOLD TO SCROLL`, not `HOLD TO WORK`. The card said "work" because the card was the game talking
to the player. This line is the *terminal* talking, and the terminal is the thing already doing the
work — so the only instruction left for the player is the slacking. It also removes a small
collision: the laptop said `HOLD TO WORK` directly above a screen full of work happening without
you. 14 characters, inside the 17-character budget.

**Alert mode** (`.turning`, `.red`, `.caught`) — the terminal is **interrupted**. The screen slams
to a full-bleed panel carrying the poster word at double height, and nothing else.

**No countdown bar.** This document originally specified a hard-edged rectangle fuse draining on
`phaseProgress` through `.turning`. It is cut. The reaction window is already on screen twice —
the mesh interpolating and, more importantly, Paul physically rotating — and a third copy of the
same clock, on the one surface the player is explicitly *not* meant to be studying during those
0.35 seconds, competed with the word instead of supporting it. `LET GO` is the signal; a bar
underneath it invited the player to read the bar. `phaseProgress` stays on `LaptopState`,
deliberately unread, because it is the one piece of engine state a timed alert would need and
re-deriving it later would mean touching the view again.

Per the design language the slam **does not ease**: there is no `.animation` modifier anywhere on
this layer, so the transition is frame-exact and costs the 0.35s reaction window nothing.

**Which phases the phone can cover, worked out rather than assumed.** The phone occupies the
rightmost 40 of the laptop's 78 columns at the same cell size, full height. But it is only up while
`isHolding`:

| Phase | Phone up? | Space available | Copy |
|---|---|---|---|
| `.turning` | **yes** — releasing is the whole task | left ~34 px of the well | `LET` / `GO`, double height, two lines — 22 × 22 px. Fits. |
| `.red` | no — holding during red is an instant catch | full 70 px | stare line, single height, wrapped over 2–3 lines (`PAUL SEES EVERYTHING` is 20 chars) |
| `.caught` | no — `endRun()` clears `isHolding` | full 70 px | `CAUGHT`, double height, 46 px wide |

So only `.turning` is space-constrained, and `LET GO` is short enough to survive it. This is the
detail most likely to be got wrong by building the alert panel centred and discovering later that
the phone sits on top of the one cue the player must see.

**Palette** — a nested `private enum` in the file, following `RunnerPalette` / `FeedPalette`. A
faithful Claude Code terminal look: near-black ground, warm tan/orange accent, muted grey for tool
output, green for a pass. `alarm 0xFF4D3D` is reserved for the alert panel and appears nowhere in
working mode. Per `PhoneScreenSim.swift:118-120`, **value separation matters more than hue at this
size** — the runner shipped broken the first time precisely because its whole palette sat at one
value.

Use fresh `unit(_:seed:)` noise offsets that don't collide with the runner's or the feed's.

### `Views/LaptopDeskView.swift` — new

One `Canvas`, structurally a near-copy of `Views/PhoneHandView.swift`.

**Grid: 78 columns × 52 rows**, `shadowOffset = 2`.

| Part | Extent |
|---|---|
| Lid | cols 2…75, rows 0…34 |
| Screen well | cols 4…73, rows 2…31 — **must equal `LaptopScreenSim.columns/rows`** |
| Hinge | row 35, cols 2…75 |
| Deck | rows 36…51, trapezoid widening from cols 2…75 at the hinge to 0…77 at the front edge |
| Keys | 2×2 blocks with 1px gutters; trackpad slab centred on the front third |

**The lid is deliberately wider than 16:10** — 70 × 30 is 2.3:1. It reads as a lid tilted back and
foreshortened, which is what you actually see looking down at a laptop on a desk, and it is what
buys the character budget. Same category of decision as Paul's 62° yaw cap: settled by looking at
it, not by reasoning from the spec sheet.

Everything else is inherited convention:

- 1-art-pixel `0x1A1A1A` outline throughout.
- Chassis reuses `PhoneHandView`'s `chassis 0x2B363C` and `chassisDeep 0x191F2B` — Paul's jacket
  tones, measured from `PaulFront.png`. Do not invent a grey. See *Asset pipeline* in
  `build-plan.md` for why the source art can't be sampled by eye.
- The **hard, zero-blur ink shadow**: composite the whole frame into one `PixelGrid`, then draw it
  twice — pass one flat `0x141019` displaced by a whole 2 art pixels, pass two in real colour
  (`PhoneHandView.swift:74-99`). Whole pixels, because a half-pixel offset on a lattice this coarse
  reads as a smear.
- Run-merged row fills via `PixelCanvasLayout.rect(column:row:width:)` (`Game/PaulSprite.swift:148`),
  which exists for exactly this.
- `.allowsHitTesting(false)` — the hold gesture is attached at the root and must not be intercepted.
- `.accessibilityHidden(true)` — see the exception below.

### `Views/PaulGameView.swift` — the only edited file

- **Remove `statusCard(now:caught:)` from the HUD `VStack`** (`:100-108`). Leave the function and
  its `statusIcon` / `statusTitle` / `statusDetail` / `statusTint` / `statusSize` helpers
  (`:278-370`) in place: `statusTitle` and `stareLine` now feed the laptop's alert panel, and an
  unused-but-intact view is what makes the accessibility exception a one-line revert.
- **Insert `laptop(now:)` in the `ZStack` between the HUD `VStack` and `phone(now:)`** (`:110`), so
  the phone rises *over* the laptop and both sit behind `nerveBadge` and `gameOver`.
- Two `@State`: `laptopSeed`, `laptopStart`. Seed them in `.onAppear` **and** on run start. A
  mirrored rising-edge `onChange(of: engine.isHolding)` is not enough on its own — the game opens in
  `.idle` with `isHolding` already `false`, so that handler never fires before the first touch and
  the laptop would render from an uninitialised seed.
- **The cell size must equal the phone's**, or the two props read as two artworks:

  ```swift
  let phoneCell = max(3, (geo.size.height * 0.34 / CGFloat(PhoneHandView.rows)).rounded())
  let cell = min(phoneCell, floor(geo.size.width / CGFloat(LaptopDeskView.columns)))
  ```

  The clamp matters: 78 columns is nearly the full width of a phone. Checked at three sizes —
  393×874 → cell 5 (390 × 260pt, 30% of height); 375×667 → cell 4 (31%); 320×568 → cell 3, where
  the width clamp is what stops it overflowing.
- Reduce Motion: the laptop is always present, so there is no slide to suppress. Gate any entry
  animation to a crossfade, following `phone(now:)`'s pattern (`:401-431`).

---

## Two consequences recorded deliberately

**1. This deletes the play screen's accessibility.** `statusCard` is the only VoiceOver-readable
game-state element (`PaulGameView.swift:316`, `.accessibilityElement(children: .combine)`) and the
only Dynamic-Type-responsive text on the screen. Its replacement is a pixel canvas that is
`.accessibilityHidden(true)`. `plan.md:154` sets an explicit bar — "this is an accessibility
workshop's own app, so it should be exemplary" — and this falls below it.

This was raised and chosen anyway, in favour of immersion. It is recorded here as a **known,
deliberate exception, not an oversight**, so that Phase 9 reopens it as a decision rather than
discovering it as a bug. **The revert is one line:** put `statusCard(now:caught:)` back in the HUD
`VStack`. If Phase 9 wants the immersion *and* the bar, the shape is an invisible
`.accessibilityElement` behind the laptop carrying label and value, plus a fallback to the glass
card at accessibility text sizes.

**2. This is a second warning channel, on purpose.** Phase 0 deferred threat-reactive props to
Phase 9 on the grounds that they duplicate Paul's signal. Making the laptop the status display
makes the duplication the point — it *is* the readout now, so it must react. It therefore inherits
the grayscale test: **the alert state must be legible by word and layout, never by red alone.**
With the fuse cut this rests entirely on the double-height word, which does survive a grayscale
screenshot — but the margin is thinner than it was, so the grayscale check in *Test* is now the
one that can fail, not a formality.

---

## Out of scope

Any change to `GameEngine`, `DifficultyCurve`, scoring, phase timing, or the catch rules — the
engine is not touched. No new entries in the asset catalog; everything is drawn in code. No audio
(Phase 5 owns it, and keystroke sound would compete with the turn cue, which `build-plan.md` Phase 5
treats as a primary game signal, not decoration). No change to the phone layer beyond the font
call-through. No menu, no game-over relayout.

---

## Test

- **Read it at rest.** Launch and don't touch anything. The laptop is present before the first
  touch, the terminal is already mid-session, and **Paul is not covered** — `plan.md:45`'s hard rule.
- **Hold.** The phone rises *over* the laptop, the terminal keeps running behind it.
- **Watch a full cycle.** On `.turning` the alert panel slams in with no easing and the fuse drains.
  **Check the word is readable with the phone up** — this is the failure this document exists to
  prevent. On `.red` the stare line has the full well. Get caught: the game-over panel still reads.
- **Press directly on the laptop art** and confirm the hold registers.
- **Toggle Reduce Motion** — nothing should slide.
- **Grayscale test** (Settings → Accessibility → Color Filters). Play a full run. With the fuse
  cut, `LET GO` / the stare line / `CAUGHT` are the *only* thing carrying the alert. If any of them
  is unreadable in grayscale, colour is doing work it shouldn't be — and the fix is the word, not
  the red.
- **Count the characters.** Every terminal line ≤ 17. Screenshot and check no glyph is clipped at
  the right edge of the well.
- **Put it beside `PaulFront.png`** and check outline weight and cell size actually match — the
  whole premise is that it reads as one artwork, and this is the check Phase 0 recorded as the one
  that caught its own mistakes.

---

## Assumptions

- **I'm assuming the laptop is yours, not Paul's.** It sits between you and him, front-on, as your
  desk. If it should be *his* workstation the whole fiction inverts — Claude would be doing his work,
  not covering for you — and the placement would move behind him.
- **I'm assuming the terminal is fiction and never shows real state.** No real filenames, no real
  build output, nothing that could be mistaken for the app reporting on itself.
- **I'm assuming a recognisable Claude Code recreation is intended and wanted**, rather than a
  generic AI agent. This knowingly breaks Phase 0's rule for on-screen content ("deliberately
  generic: no branding, no likeness, original palette"), which was written for the phone's mini-apps
  where branding would have been noise. Here the recognition *is* the joke. Worth a second look
  before shipping, since `AppStore/` exists and this is a public release rather than a workshop
  demo — say if it should be a generic agent and the copy changes, nothing else does.
- **I'm assuming the accessibility exception above is accepted** with Phase 9 free to reopen it.
- **I'm assuming a per-run seed rather than per-hold.** The laptop is continuous — it doesn't arrive
  and leave the way the phone does — so its session should persist across holds and reset only when
  a run does.
- **I'm assuming 4 terminal lines is enough** to read as a working agent. If it isn't, the honest fix
  is a taller lid, not a smaller font — the shared cell size is the one thing that must not move.

---

## Remaining work

Written after the build, as the honest state of it.

1. **Nothing has been compiled or run.** All four files are written and wired, but no build has
   happened in this environment — `xcodebuild` was not available to check. Build and fix what falls
   out before trusting a line of this. The likeliest snags are the `Group { let showing = … }` in
   `phone(now:cell:)` and the `LaptopState` initialiser call in `laptop(now:cell:)`. The project
   uses Xcode file-system-synchronised groups, so the three new files need no `.pbxproj` edit.
2. **Two loose ends in `PaulGameView`.** There are now two consecutive `.onChange(of: engine.phase)`
   handlers — the new laptop reseed and the existing stare-line draw — which should be one. And
   `phone(now:cell:)`'s doc comment still says the phone "sits in front of the status card"; that
   card is gone, and what it now covers is the laptop's right half.
3. **Every check in *Test* is still unrun.** They were reasoned through on paper, not seen. The
   three that can actually fail are: **Paul not covered** at 393×874 and 375×667 (the HUD stack
   reserves `LaptopDeskView.rows × cell` at the bottom, which is arithmetic, not an observation);
   **`LET GO` readable with the phone up**, which is the failure this document exists to prevent;
   and the **17-character count**, which needs a screenshot at the right edge of the well rather
   than a count in the source.

Two smaller things worth knowing, neither blocking:

- The laptop bleeds ~10pt off the right edge on a 393pt-wide screen, because the drawn frame is
  `columns + shadowOffset` = 80 cells while the clamp in *Build* sizes against 78. The deck already
  runs off both edges by design, so this reads as intended rather than as an overflow — but it is
  arithmetic that was chosen, not inherited.
- On a 320×568 screen the HUD stack overflows. It did so before this document too, because Paul is
  a fixed 320pt square; this makes it worse rather than causing it.

---

## Where this sits in the build order

Nowhere in `build-plan.md`'s numbering, by request. But it should be read against that document's
own sequencing note: the critical path is still **the outstanding half of Phase 2** — the fake-out
ramp bug, the restart path, the unit tests, and above all the on-device feel test that answers
`plan.md`'s standing warning, *"if holding-and-releasing doesn't feel good, everything after this is
wasted."*

Phase 0 earned its slot ahead of that by being cheap, additive, and blocking nothing. This is
larger — a font, a second sim, a new prop, and a HUD change that deletes a card — and it is not
purely additive. That's not an argument against building it, but it is worth stating plainly rather
than letting it happen quietly.
