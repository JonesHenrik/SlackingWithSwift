# Slacking with Swift — Build Plan

> Companion to `plan.md`. `plan.md` says *what the game is*; this file says *what we build, in
> what order, and how we know each step worked*.
>
> **Status:** written 2026-08-12. Updated 2026-08-12 — **the design is chosen.** It is not one of
> the four: it's a merge of **Liquid Glass** (kept nearly whole) and the **Brutalist** Paul figure,
> shipped as `Views/PaulGameView.swift` + `Views/PaulFigureView.swift`. Real front/back sprite art
> landed at the same time. See *The design language* below, which is now filled in, and Phase 3,
> which is now partly done rather than blocked.
>
> Updated 2026-08-18 — **a new Phase 0, "The phone in your hand," is inserted at the front and
> every previously-numbered phase moved up one (old 0–8 are now 1–9).** It is a cosmetic
> overlay: a pixel-art hand and phone that rise into frame while you hold. References to
> `plan.md`'s own phase numbers are unaffected — that document still numbers 1–6, plus its
> own new Phase 0.

---

## What I found in the repo

`plan.md` opens with "The directory is empty — this is greenfield." That is no longer true. A
significant amount of the game already exists, but **none of it runs**. Reconciling those two
facts is what Phase 1 and Phase 2 are for.

### What exists and is good

| File | State |
|---|---|
| `Game/GameEngine.swift` | Real, complete phase machine. Deadline-driven `Task.sleep`, no tick loop, event-driven catch detection. Matches `plan.md`'s timing architecture exactly. |
| `Game/DifficultyCurve.swift` | All tuning constants in one struct, plus a closed-form score integral so score never depends on a timer firing. Matches the plan. |
| `Game/PaulSprite.swift` | Four poses as 16×18 character grids + `PixelSpriteView`, a palette-driven `Canvas` renderer. The programmatic 8-bit Paul the plan asked for. |
| `Styles/` | Four complete, independent full-screen game views + `GameStyle.swift` (enum, swatches, taglines, shared `holdSurface` gesture). |

### What's missing or wrong

1. ~~**The app does not run the game.**~~ **Resolved 2026-08-12.** `ContentView` now hosts
   `PaulGameView` directly and the game is playable on launch. Note this was resolved *differently
   than Phase 2 planned*: because the design got decided directly, no `RootView` and no style
   gallery were ever built. There is still no menu — the game starts on first touch, and game-over
   offers "AGAIN". Extracting a menu is now Phase 3 work.
2. **Nothing is committed.** Only the bare Xcode template is in git (`c29bfc4`). All of `Game/`
   and `Styles/` is untracked, alongside `.DS_Store` and `xcuserdata/`.
3. **Deployment target is iOS 26.5**, not the iOS 17 the plan specifies. That restricts install
   to devices on the very latest OS — a real risk for a party game passed around a room of
   mentors' phones. `SWIFT_VERSION` is also still `5.0`.
4. **Fake-out is implemented differently than the plan describes.** The plan calls it "a twitch
   ~30% into a turn that snaps back." The code makes it a *separate phase that replaces the turn
   entirely* — and because `cycle += 1` only runs after a completed RED, **a fake-out does not
   advance the difficulty ramp.** A run with many fake-outs stalls at low difficulty. Also, its
   0.45s duration is hardcoded in `GameEngine`, breaking the "every constant lives in
   `DifficultyCurve`" rule.
5. **There is no restart path.** `start()` doesn't reset `phase`, so recovering from `.caught`
   requires calling `reset()` *then* `start()`. Nothing currently does. Wiring this is Phase 2.
6. **The file layout doesn't match the plan's.** No `GamePhase.swift` (the enum lives inside
   `GameEngine.swift`), no `ScoreKeeper.swift` (scoring is split across `DifficultyCurve` and the
   engine), no `Views/`, no `Services/`. I consider the *actual* layout better and propose keeping
   it — the plan's split was speculative and the current version is cohesive.
7. **Whole plan areas are unbuilt:** audio, haptics, `LeaderboardService`, Game Center, assist
   mode, Dynamic Type, VoiceOver, and a dedicated game-over/menu surface. `bestScore` in
   `UserDefaults` is a single-entry stand-in for the local leaderboard.
8. **Accessibility is the weakest area, which is awkward for an accessibility workshop's own app.**
   `PixelSpriteView` is `.accessibilityHidden(true)`, so Paul — the primary non-color signal —
   is invisible to VoiceOver. Only `LiquidGlassGameView` honors Reduce Motion; `ArcadeCRTGameView`'s
   `ShakeEffect` is ungated. There are no audio or haptic cues at all, so `plan.md`'s "play with
   your eyes closed" test currently fails outright.

   **Partly addressed 2026-08-12** in the shipped design only (the four old styles are unchanged):
   `PaulFigureView` exposes an accessibility value announcing Paul's orientation; Reduce Motion is
   honored (rotation, sway, lunge, scale and mesh drift all drop out); haptics are wired via
   `.sensoryFeedback` on turn / caught / nerve bonus. **Contrast was a real bug and is fixed:** in
   the RED phase the glass panels render pale pink, so the light type on them was failing 4.5:1.
   The HUD cards now slam to `ink` alongside the screen, and the secondary-text opacities were
   raised. Audio is still absent, so the eyes-closed test still fails — that's Phase 5.
9. **Tests are empty Xcode templates.** `DifficultyCurve`'s scoring math is pure, deterministic,
   and the highest-value thing in the codebase to unit-test — it's currently untested.
10. ~~`paul.jpg` sits at the repo root, unreferenced by code.~~ **Superseded 2026-08-12.** The art
    situation is now: `PaulImage.png` (a single crossed-arms portrait, **no longer used**) and
    `PaulFrontBack.jpeg` (a front + back sprite sheet, **now the shipping art**). Both sit at the
    repo root as sources; the game consumes cut-down `PaulFront` / `PaulBack` imagesets. See
    *Asset pipeline* below — this is the part most likely to trip up whoever adds the next frame.

---

## The design language — "Haunted Glass"

**Decided 2026-08-12.** The winner is not one of the four. It's a **merge**: Liquid Glass kept
nearly whole for the environment and HUD, and the Brutalist treatment of the Paul figure kept for
the menace. The reasoning is that Liquid Glass was the better *screen* and Brutalist had the better
*character* — the mistake would have been picking one and inheriting the other's weakness.

Shipped as two files, `Views/PaulGameView.swift` (screen) and `Views/PaulFigureView.swift`
(character), over the untouched `GameEngine`.

### Palette

| Token | Hex | Role |
|---|---|---|
| `calm` | `0x8AD8C6` | mint; safe state, disc behind Paul at rest |
| `lilac` | `0xB9A7F5` | mesh mid-tone |
| `alarm` | `0xFF4D3D` | danger. Hotter than Liquid Glass's original `0xFF7A6B` |
| `ink` | `0x141019` | type, hard shadows, slammed cards. Deeper than the original `0x1B2340` |
| `bone` | `0xF4F1EA` | Brutalist paper, carried over as light type on dark |

`PaulSprite`'s `h`/`s`/`t`/`e`/`w` legend **no longer applies to the shipped design** — that legend
maps the programmatic pixel grid, and Paul is now real raster art. The legend still matters to the
four old styles until Phase 3 deletes them.

### Threat expression — the core hook

`engine.threat(at:)` (0 → 1) drives everything, so one value keeps the whole screen in sync:

- **Mesh gradient** warms toward `alarm` *and loses value*. This is the one change to Liquid Glass:
  on its own it stayed too pretty to be frightening, and pulling the background darker is what lets
  the figure read as menacing on top of it.
- **Paul** rotates, brightens out of shadow, and his eyes ignite (below).
- **The disc** behind him blooms `calm` → `alarm` and scales up.
- **The reaction meter** drains during `.turning` only.

**RED does not ease.** The mesh interpolates through the *turn*, because that interpolation is the
player's information. But the instant Paul is looking, a flat `alarm` wash appears with no animation
modifier anywhere on that layer. Abruptness is the whole point of that phase, and it's the single
most Brutalist thing that survived into the merge.

### Sprite treatment

`PixelSpriteView` is unused by the shipped design. Paul is two raster frames swapped 2.5D:

- He rotates about his own vertical axis; at the halfway point the back frame is replaced by the
  front frame and rotation continues in the same direction, so it reads as one turn, not a cut.
- **Yaw is capped at 62°, deliberately short of 90°.** At 90° the sprite foreshortens to an
  unreadable vertical sliver, and body orientation is the player's primary signal for the entire
  game. This was found by looking at it, not by reasoning about it.
- **Hard, zero-blur offset shadow** at `(12, 12)` — a second copy of him, like a printing
  misregistration. Straight from Brutalist; it makes him sit *on top of* the glass, not inside it.
- **Shadow on his back** while turned away (32% `0x0B0710`), lifting as he comes round, so the
  reveal has somewhere to travel. This replaces Brutalist's full void now that the back art is real.
- **The eyes are the payload.** Two hot points ignite in his lenses across the second half of the
  turn, slightly ahead of the rest of him. Iris positions are *measured from the asset*
  (`0.4921, 0.1532` / `0.5515, 0.1530`, normalised) rather than eyeballed, and live as constants at
  the top of `PaulFigureView`.
- `.interpolation(.none)` on every frame, per `plan.md`.

### Type

SF Rounded throughout (Liquid Glass), but at Brutalist weight and tracking — `.black` with negative
tracking, set *inside* the soft glass cards. Soft container, hard type. Size ramp: score 46,
status word 40 when `.turning`/`.red` and 26 otherwise (the turn and the stare get poster scale,
nothing else does), game-over score 72, labels 11–13 with wide positive tracking.

### HUD layout

Header glass card (score / multiplier / best / optional close), Paul centred, status glass card at
the bottom (icon + poster word + detail line + meter + holding state). The meter is the one place
the poster language wins outright: a **hard-edged rectangle, not a capsule**, because a soft capsule
reads as "progress" and this is a fuse.

### Motion, and what Reduce Motion drops

Rotation, idle sway, the caught lunge, threat-driven scale, and the mesh drift are all suppressed;
the reveal degrades to a plain crossfade and the turn stays readable. **No `.animation` modifier on
the figure** — `reveal` changes every frame inside a `TimelineView`, and an implicit animation would
fight the frame-accurate value and add lag to a 0.35s reaction window.

**What survives regardless:** `GameEngine`, `DifficultyCurve`, the `holdSurface` gesture, and
`Color(hex:)`. `PaulSprite` / `PixelSpriteView` survive only as long as the four old styles do.

---

## Asset pipeline

**Read this before adding any sprite frame.** The source art cannot be dropped into the asset
catalog as-is, and the failure mode is silent and confusing.

**The trap:** both `PaulImage.png` and `PaulFrontBack.jpeg` have the transparency checkerboard
**baked into the pixels**. `PaulImage.png` advertises an alpha channel, but every pixel is alpha
255 — the checkerboard is real grey artwork, not transparency. Dropped in raw, Paul renders as a
solid grey rectangle, and any silhouette or template-rendered treatment becomes a solid black box.
Previewers draw their own checkerboard behind transparent images, so **eyeballing a preview cannot
tell you whether an asset is actually transparent** — check the alpha values.

**The fix**, automated in `Tools/split_sprite_sheet.py`:

1. Flood-fill from the borders, treating low-saturation bright pixels as background. Flood-fill
   rather than global colour-keying, so light greys *inside* the figure survive.
2. Erode the pale fringe (3 passes) — JPEG ringing leaves a halo, and the source art also has a
   white sticker outline that has to go with it.
3. Split the sheet, crop each figure to its own bounding box.
4. **Re-register both frames onto one shared square canvas, aligned on a common baseline.** This is
   the step that matters most: if the frames aren't registered, Paul visibly jumps at the mid-turn
   swap. Both current frames came out 850px tall from the same sheet row, so they align exactly.
5. Report measured iris positions, which get pasted into `PaulFigureView`.

Output: `PaulFront` / `PaulBack` imagesets, single 1x slice on an 874×874 canvas. Re-run the script
rather than hand-editing assets, and re-paste the iris constants if the crop changes.

---

## Phase 0 — The phone in your hand

The game's fiction is "slack off while Paul isn't looking," but the thing you are supposedly
*doing* while you hold has never been on screen. This phase puts it there: while the player
holds, a pixel-art hand holding a phone slides up from the bottom-right corner, and the phone
plays a live, procedurally-animated mini-app. Release and it slides back down. It is the one
phase in this plan that is pure flavour — it is here first because it is cheap, it is entirely
additive, and it makes the premise legible to someone watching over your shoulder.

**Build:**

- `Game/PhoneScreenSim.swift` — `enum PhoneApp { case runner, feed }` plus a pure
  `render(_:elapsed:seed:)` that returns a grid of art pixels. **No state, no timer**: every
  frame is a function of elapsed seconds and a per-hold seed, so it inherits `PaulGameView`'s
  existing `TimelineView(.animation)` and does not violate the no-tick-loop rule.
  - `.runner` — three scrolling lanes, a 5×6 blob with a two-frame run cycle, hop-based lane
    changes on a deterministic schedule, obstacle blocks growing as they approach, coin dots,
    and a 3×5 micro digit font for the score. Endless-runner *shaped*, deliberately generic:
    no branding, no likeness, original palette.
  - `.feed` — a stack of posts (avatar block, grey text bars, flat-hue image block, reaction
    row) scrolling up continuously with periodic flick bursts that decelerate and settle; a
    heart reddens as it passes mid-screen. Same rule: generic, no logos.
- `Views/PhoneHandView.swift` — one SwiftUI `Canvas` on a ~40×62 art-pixel grid: chassis and
  outline, the screen well filled from `PhoneScreenSim`, then fingers and a thumb over the
  lower-right of the screen, plus the hard zero-blur offset shadow the figure already uses.
  `.allowsHitTesting(false)` — the hold gesture is attached at the root and must not be
  intercepted. Follow `PixelSpriteView`'s cell math (`Game/PaulSprite.swift`); it can be
  generalised past its hardcoded 16×18 rather than duplicated.
- `Views/PaulGameView.swift` — three `@State` properties (app, seed, start date) set on the
  rising edge of `engine.isHolding`, and one layer inserted between the HUD `VStack` and
  `nerveBadge`. Visibility is driven purely by `isHolding`; slide is a spring on `.offset`,
  suppressed to a crossfade under Reduce Motion.

**The art must match Paul, not merely coexist with him.** Hand, chassis and mini-app all draw
on *one shared coarse pixel grid* — a shared cell size is what stops this reading as a vector
UI pasted over pixel art — with a 1px `#1A1A1A` outline and skin/slate tones sampled from
`PaulFront.png` rather than invented. See *Asset pipeline* above for why the source art can't
be trusted by eye.

**Out of scope:** Any change to `GameEngine`, `DifficultyCurve`, scoring, phase timing, or the
catch rules — this phase is cosmetic and the engine is not touched. No HUD relayout. No new
assets in the catalog (everything is drawn in code). No reaction to the danger phase.

**Test:** Hold and release repeatedly — the hand arrives in ~0.25s with the screen already
animating, retracts on release, and the mini-app alternates between runner and feed across
holds. Hold through a full turn until caught: `endRun()` already clears `isHolding`, so the
phone should retract as the game-over panel fades in. Start a press *on* the phone art and
confirm the hold still registers. Toggle Reduce Motion and confirm it crossfades. Then put
it beside `PaulFront.png` and check outline weight and pixel size actually match.

**Assumptions:**
- **I'm assuming covering the status card is intended.** At ~35% of screen height in the
  bottom-right, the phone sits in front of the status card and partly hides the "LET GO"
  warning while holding. That was chosen deliberately — being distracted is the joke, and
  Paul himself stays fully visible, which is the signal that actually matters. Say if the
  warning should win and I'll drop the phone behind the card instead.
- I'm assuming the mini-apps stay **oblivious to threat** — they play identically whether
  Paul is turned away or staring. Tinting them red would be a second warning channel; that
  belongs to Phase 9 if it belongs anywhere.
- I'm assuming a random app per hold rather than one per run, so a long session sees both.

---

## Phase 1 — Foundation and decisions

**Build:** No gameplay change. Get the repo into a state where work is trackable.

- Add a `.gitignore` (`.DS_Store`, `xcuserdata/`, `build/`, `DerivedData/`).
- Commit the existing untracked `Game/` and `Styles/` work as a baseline.
- Resolve the two settings decisions in *Assumptions* below.
- Delete the template `ContentView.swift` (Phase 2 replaces it with `RootView`).

**Out of scope:** Any game logic, any UI, any new files beyond `.gitignore`.

**Test:** `git status` is clean apart from intended files. The project builds and launches (to a
blank screen — expected at this point).

**Assumptions:**
- **I'm assuming the iOS 26.5 deployment target was Xcode's default, not a deliberate choice, and
  I should lower it to iOS 17** per `plan.md`. If the mentors are all on the latest OS, say so and
  I'll leave it. This is the one item here I'd like a yes/no on.
- I'm assuming `SWIFT_VERSION 5.0` should stay for now. The code is already `@MainActor`/`@Observable`
  clean, so Swift 6 language mode is likely a small step, but it's not worth a migration mid-build.
- I'm assuming you want this on `main` as normal commits, not a branch + PR.

---

## Phase 2 — Make it playable, and pick the winner

> **Status 2026-08-12: partly overtaken.** The design question got answered directly (see *The
> design language*), so the style gallery this phase proposed was never built and is no longer
> needed. The app is now playable on launch via `ContentView` → `PaulGameView`.
>
> **Still outstanding from this phase, and still the highest-value work in the plan:** the fake-out
> ramp bug, the restart path, the unit tests, and — above all — the on-device feel test. Choosing a
> design does *not* discharge `plan.md`'s warning. Nobody has yet confirmed that
> holding-and-releasing is fun on real hardware.

This is `plan.md` Phase 1, and its warning stands: **if holding-and-releasing doesn't feel good,
everything after this is wasted.** This phase exists to answer that question and the design question
at the same time, on a real device.

**Build:**

- `RootView.swift` — routing between menu, game, and game-over. Replaces `ContentView`.
- Wire `PaulGameApp` → `RootView`.
- A **temporary** style gallery: the four `GameStyle` cards using the existing `swatch`, `title`,
  and `tagline`. The existing `onExit` closure on every style view already plugs straight in.
- Fix the restart path so game-over → play again works (`reset()` then `start()`), and so the run
  actually begins on first touch.
- Fix the fake-out cycle bug: a fake-out should advance the difficulty ramp. Move its 0.45s duration
  into `DifficultyCurve`.
- Unit tests for `DifficultyCurve` (see *Test* below).

**Out of scope:** Audio, haptics, Game Center, real art, assist mode, deleting any style, any new
visual design. Difficulty *tuning* is Phase 4 — this phase only fixes the structural bug, it does
not change the numbers.

**Test:**

- **Unit (fast, no device):** `score(forHoldOf:)` is continuous across the multiplier cap boundary
  (`capTime = 8s` — assert no jump at 7.99 → 8.01); one continuous 2s hold scores strictly **more**
  than two separately-banked 1s holds, which is the entire design thesis and deserves an explicit
  assertion; `multiplier` clamps at 5; `ramp` clamps at 1.
- **On device (the real test):** all four styles launch, are playable, and return to the gallery.
- Play a cautious run (tap-and-release immediately) and a nervy run (ride each window). Per
  `plan.md`: cautious ≈ 2–3k, nervy 5–10× that. **If both strategies score similarly, stop and fix
  the multiplier before proceeding.**
- Confirm a fake-out can never cause a catch.
- Get caught, restart, get caught again — no stuck states, no ghost timers from the previous run.

**Assumptions:**
- **I'm assuming the gallery is throwaway** and gets deleted in Phase 3 rather than shipping as a
  player-facing theme picker. Say if you'd rather keep it as a feature.
- I'm assuming each style's existing self-contained game-over UI is good enough for now, so
  `GameOverView` doesn't need to be extracted until Phase 3.
- I'm assuming "fake-outs should advance the ramp" is the right reading of the plan's intent. The
  alternative — fake-outs are free and don't count as a cycle — is defensible; I'll go with
  advancing unless you say otherwise.

---

## Phase 3 — Design lock-in  ✅ *unblocked; roughly half done*

**Done 2026-08-12:** the winning design is built and running (`Views/PaulGameView.swift`,
`Views/PaulFigureView.swift`), `Views/` exists alongside `Styles/`, the design language section
above is filled in from shipped code, and the real art is integrated.

**Build (remaining):**

- **Delete the four style files**, the `GameStyle` enum, and the swatch/tagline metadata. They still
  compile and are unreachable from the app. `PaulGameView` takes an *optional* `onExit`, so it can
  be dropped back into a gallery if you'd rather keep them a while — that's the only reason they're
  still here.
- Move `Color(hex:)` and `holdSurface` out of `GameStyle.swift` before deleting it. **Both are
  load-bearing for the shipped design**, so this is the one step that can break the build.
- Decide the fate of `PaulSprite.swift` / `PixelSpriteView`. Nothing in the shipped design uses
  them; they die with the old styles unless you want the programmatic Paul as a fallback.
- Extract `GameOverView.swift` and add a menu — the game currently starts on first touch with no
  front door.

**Out of scope:** New features. This is consolidation only — the game should play *identically*
before and after, just with 75% less view code.

**Test:** Full playthrough is visually and behaviorally unchanged from the winner in Phase 2.
`grep` finds zero references to the three deleted styles. The app builds with no warnings. Phase 2's
unit tests still pass untouched (they don't know about views — if they break, the split was wrong).

**Assumptions:**
- ~~I'm assuming exactly one of the four wins.~~ **Wrong — it was a merge of two**, which is why
  this phase grew a build step instead of being pure deletion. Worth noting for next time: the
  gallery's real value was making the *comparison* possible, not picking a winner outright.
- I'm assuming you want the losers **deleted**, not commented out or feature-flagged. Nothing is
  committed yet, so unlike the original plan they are **not** recoverable from a Phase 1 commit —
  commit before deleting.

---

## Phase 4 — Tune

`plan.md` Phase 2. Playtesting, not programming.

**Build:** Iterate on `DifficultyCurve` values. Optionally a DEBUG-only tuning panel (sliders bound
to the curve) so tuning doesn't need a rebuild per change.

**Out of scope:** Any change to `GameEngine`'s structure. If tuning requires an engine change, the
mechanic is wrong and that's a Phase 2 conversation, not a Phase 4 one.

**Test:** `plan.md`'s criterion is the only one that matters — the gap between a cautious run and a
nervy run must be large and legible. Play on **real hardware**; simulator input latency will lie to
you about a 0.35s window. Recruit one person who has never played and watch where they get caught.

**Assumptions:** I'm assuming the plan's numbers are a starting point, as it says. I'm assuming the
debug panel is worth building — if you'd rather just edit constants and rebuild, say so and I'll skip it.

---

## Phase 5 — Feel: audio and haptics

`plan.md` Phase 3. **Note the ordering consequence:** the plan lists accessibility last, but the
audio built here *is* the non-visual channel that "play with your eyes closed" depends on. So this
phase builds audio as a primary game signal, not as decoration.

**Build:**

- `Services/AudioPlayer.swift` — `AVAudioSession` on `.ambient` + `.mixWithOthers`, so it doesn't
  kill the player's music.
- Distinct cues for: turn beginning (the critical one), caught, and nerve bonus.
- Haptics via `.sensoryFeedback` on the same events.

**Out of scope:** Music. Volume/mix settings UI. Anything requiring a sound designer.

**Test:** Turn cue fires at the *start* of `.turning`, with no perceptible lag against the visual.
Music from another app keeps playing at full volume underneath. Silent switch behaves sanely.
Haptics fire on device (they no-op in simulator). **Then the real test: play a full run with the
screen face-down.** If you can survive several cycles on audio alone, the channel works.

**Assumptions:** I'm assuming I should generate simple synthesized tones rather than source audio
assets. I'm assuming iPhone-only for haptics (iPad has no haptic engine) and the code should degrade
silently there.

---

## Phase 6 — Local leaderboard

Pulled *earlier* than `plan.md`'s ordering, deliberately: the plan already specifies the
`LeaderboardService` protocol with a local implementation that "works day one." Building it before
Game Center means the app is feature-complete and demoable with **zero** external dependencies.

**Build:** `Services/LeaderboardService.swift` — the protocol plus `LocalLeaderboard`
(`UserDefaults`, top ~10 with names). `LeaderboardView` rendering it. Score submission on game over.

**Out of scope:** Game Center, authentication, anything network. Anti-cheat — `plan.md` is explicit
that we deliberately build none.

**Test:** Scores persist across app relaunch. Ordering and the top-N cap are correct. Ties are
handled. A fresh install shows a sensible empty state.

**Assumptions:** I'm assuming a local leaderboard needs a player name, so there's a one-time name
prompt. I'm assuming top 10 unless you want a different depth.

---

## Phase 7 — Art  ✅ *first pass done; more frames optional*

`plan.md` Phase 4. Independent of every other phase — it can slot in whenever the sprites arrive.

> **Status 2026-08-12: art landed early and is shipping.** `PaulFrontBack.jpeg` gave two frames —
> front and back — which is enough for the whole game, because the turn is rendered as a **2.5D
> rotation with a mid-turn frame swap** rather than as an animation sequence. That was a deliberate
> trade: two frames plus rotation beats waiting for nine. `GameEngine.pose(at:)` is untouched; the
> shipped figure drives off `threat(at:)` directly for a continuous turn.
>
> **If more frames arrive**, the natural next additions are a caught/pointing pose (currently the
> front frame with a lunge and a saturation bump) and a true three-quarter frame to replace the
> rotated front frame at mid-turn. Neither is required. Run `Tools/split_sprite_sheet.py` — do not
> hand-cut assets — and re-check registration against the existing baseline.

**Build (if more frames arrive):** Swap real pixel art into the sprite renderer. `plan.md` specifies
back-idle (2 frames), turning (4), facing (2), caught/pointing (1) — nine frames against the four
static poses that exist today, so `GameEngine.pose(at:)` gains frame selection.

**Out of scope:** Everything else. Per the plan, the sprite renderer should be the only file that
changes.

**Test:** `.interpolation(.none)` on every `Image` — without it, scaled pixel art turns to mush; this
is the one thing that will visibly go wrong. Verify the turn animation still reads as a clear
progression at the fastest difficulty (0.35s window), where four frames is roughly 90ms each.

**Assumptions:** I'm assuming the art doesn't exist yet and `paul.jpg` is the reference photo. I'm
assuming that if art never arrives, the programmatic `PaulSprite` ships as-is — `plan.md` is clear the
game is complete without it.

---

## Phase 8 — Game Center

`plan.md` Phase 5. **This is the only phase with an external blocker**: it needs an App Store Connect
app record with a configured leaderboard ID, which depends on your team's ASC access. Nothing else in
this plan waits on it.

**Build:** `GameCenterLeaderboard` conforming to the Phase 6 protocol. Authentication, submission,
and `GKGameCenterViewController` wrapped for SwiftUI. Graceful fallback to `LocalLeaderboard` when
the player isn't signed in.

**Out of scope:** Achievements, multiplayer, challenges.

**Test:** Sign in with a **sandbox** Apple ID and confirm a score appears on the leaderboard. Then
the case that actually matters at a party: decline the Game Center prompt and confirm the game is
still fully playable against the local leaderboard.

**Assumptions:** I'm assuming ASC access is not yet arranged, so this phase gets scheduled when you
tell me it is. I'm assuming a single leaderboard now, with assist mode's separate board added in
Phase 9.

---

## Phase 9 — Accessibility pass

`plan.md` Phase 6. Given this is the Academy's own accessibility workshop, I'd treat this as
non-negotiable rather than a nice-to-have — and I'd rather move parts of it earlier if you agree.

**Build:**

- **Assist mode** — 1.5× reaction window, separate leaderboard. `plan.md` notes it also makes live
  demos safer, which matters if this gets shown on stage.
- **Reduce Motion** honored everywhere (today only one style does; the ungated shake effect in the
  CRT style is the known offender if that one wins).
- Dynamic Type on menu, game-over, and leaderboard.
- VoiceOver on all menus, and an accessibility value on the game surface that announces Paul's
  orientation — `PixelSpriteView` is currently `.accessibilityHidden(true)`, which hides the game's
  primary non-color signal.
- Verify Paul's **body orientation** plus audio/haptics carry the full signal, with **no reliance on
  color alone**.

**Out of scope:** Switch Control and Voice Control tuning, unless you want them.

**Test:** Toggle Reduce Motion in Settings and confirm the turn is still readable. Play a full run in
grayscale (Settings → Accessibility → Color Filters) — if that's impossible, color is doing work it
shouldn't. Navigate every menu with VoiceOver, eyes closed. Run at the largest accessibility text
size and confirm nothing truncates or overlaps. Confirm assist-mode scores never reach the main board.

**Assumptions:** I'm assuming assist mode is a menu toggle that persists. I'm assuming the grayscale
and eyes-closed tests are the acceptance bar, since `plan.md` names them.

---

## Sequencing summary

| Phase | Depends on | Blocked by | Status |
|---|---|---|---|
| 0 — Phone overlay | — | — | not started |
| 1 — Foundation | — | one deployment-target decision | not started — **nothing is committed** |
| 2 — Playable + pick winner | 1 | — | app runs; **feel test + fake-out bug + tests outstanding** |
| 3 — Design lock-in | 2 | ~~the design choice~~ | design built; **deletion pass outstanding** |
| 4 — Tune | 2 | device playtesting | not started |
| 5 — Feel | 3 | — | haptics done, **audio outstanding** |
| 6 — Local leaderboard | 3 | — | not started (`bestScore` stand-in only) |
| 7 — Art | 3 | ~~sprites arriving~~ | **done** — front/back shipping |
| 8 — Game Center | 6 | **App Store Connect access** | not started |
| 9 — Accessibility | 5 | — | partly done in the shipped design |

The design gate is gone. **The critical path is now Phase 1 → the outstanding half of Phase 2.**
Phase 0 sits ahead of both but depends on nothing and blocks nothing — it can be built, skipped,
or deferred without moving anything else. Two things still deserve to jump the queue:

1. **Commit something.** All of `Game/`, `Styles/`, `Views/`, the new imagesets and `Tools/` are
   untracked. The Phase 3 deletion pass is irreversible without it.
2. **Play it on a phone.** `plan.md`'s Phase 1 warning is still unanswered, and everything from
   Phase 4 onward assumes the answer is yes. The design being finished makes this *easier* to
   ignore, not less necessary.

---

## Open questions

1. **Deployment target** — lower iOS 26.5 → 17 per `plan.md`, or was 26.5 deliberate? **This is now
   more consequential than when I first asked.** The shipped design uses `glassEffect` and
   `MeshGradient`, which are not available on iOS 17. Dropping the target now means either
   reworking the glass panels or gating them behind availability checks. If the mentors are all on
   the latest OS, saying so closes this cheaply.
2. ~~**Which design wins?**~~ **Answered:** the Liquid Glass / Brutalist merge.
3. **App Store Connect access** — do you have it, and should I plan Phase 8 soon or leave it parked?
4. **Fake-outs and the difficulty ramp** — should a fake-out count as a cycle? I've assumed yes.
   Still open; still a real bug.
5. **Phase 0 ordering** — it now sits ahead of committing anything. I'd still commit the
   baseline first; that's a one-command precaution, not a reordering, and the Phase 3 deletion
   pass is irreversible without it.
6. **New — do the four old styles get deleted now?** They're dead weight but they're also the record
   of the comparison. Commit first either way.
