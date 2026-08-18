# Slacking with Swift — Red Light, Green Light

## Context

A party game for mentors at the Apple Developer Academy in Detroit who trained with Paul
Hudson. Paul has approved use of his likeness as a game character.

The framing is "don't slack off while working with Claude," but we made a deliberate call:
**this is an honest party game, not a productivity tool.** It doesn't monitor your phone
usage or pretend to help you focus. It's a fast reflex game about the in-joke of getting
caught slacking, with a Game Center leaderboard for bragging rights.

Endless survival: you play until Paul catches you. One life, instant restart.

The directory is empty — this is greenfield.

### The design problem being solved

"Hold as long as you can" is not by itself a game. If releasing early is free, the optimal
strategy is to tap and release instantly, every run looks the same, and the leaderboard is
noise. **The core design work is making it costly to be cautious**, so that high scores
require nerve. That's what the multiplier and nerve-bonus below are for — they are the
mechanic, not polish.

---

## Core loop

One cycle, repeating with rising difficulty:

| Phase | Paul | You | Rule |
|---|---|---|---|
| GREEN | back turned | hold | score accrues, multiplier climbs |
| TURN | rotating toward you | **release now** | this is your reaction window |
| RED | facing you | hands off | holding at any point here = caught |
| RETURN | turning back | wait | hold becomes safe again on GREEN |

Getting caught ends the run. Release too early and you just lose accrual time — no
penalty beyond opportunity cost.

**Fake-out:** Paul twitches ~30% into a turn and snaps back. Probability ramps from 0 to
~0.3 over the run. Costs nothing mechanically; it punishes over-reaction by burning your
multiplier, which is exactly the pressure we want.

**The phone:** while you hold, a hand holding a phone rises into frame from the bottom-right
and plays a mini-app — an endless runner or a social feed, chosen at random each hold, both
animated live rather than looped. Release and it drops away. This is the one purely cosmetic
element in the game and it should stay that way: it changes no timing, no scoring, and no
phase behaviour, it just makes the fiction literal. It deliberately sits *in front of* the
status card, because being absorbed in it is the joke; Paul himself is never covered, and he
is the signal that matters.

### Scoring — this is what makes the leaderboard competitive

- **Base:** 100 pts/second, only while holding.
- **Multiplier:** +0.5x per continuous second held, capped 5x. **Resets to 1x on every
  release.** This is the cost of caution.
- **Nerve bonus:** releasing in the final 25% of the reaction window = flat +500 and a
  "CLOSE!" flash.

Net effect: a timid player scores maybe 2–3k. A player who rides each window to the last
frame scores 5–10x that. Skill is legible on the leaderboard.

### Difficulty curve (`DifficultyCurve.swift`)

All values interpolate over the first ~20 cycles, then hold at floor:

- Reaction window (turn duration): **0.90s → 0.35s**
- GREEN duration: random in `2.5–5.0s` → `1.2–2.5s`
- RED duration: random in `0.8–1.6s`
- Fake-out chance: `0.0 → 0.30`

These are starting numbers, expected to change during playtesting. Keep them in one file
with named constants so tuning is a single-file edit.

---

## Architecture

**SwiftUI, iOS 17+** (for `@Observable` and `.sensoryFeedback`).

### Timing: no tick loop

A 0.35s reaction window will not survive timer drift. Do **not** run a per-frame timer that
mutates game state.

- Phase transitions are driven by a single `Task` using `Task.sleep(until:)` with absolute
  deadlines.
- Catch detection is **event-driven**: when the TURN phase completes, check `isHolding`. No
  polling, exact by construction.
- Score is computed from accumulated held intervals (`Date`/`ContinuousClock` math), never
  incremented per frame.
- `TimelineView(.animation)` is used **only for rendering** the HUD/sprite, never for logic.

### Input

`DragGesture(minimumDistance: 0)` on a full-screen surface — `onChanged` starts the hold,
`onEnded` ends it. Not `LongPressGesture`, which has a built-in delay that would corrupt
timing.

### Files

```
PaulGame/
  PaulGameApp.swift
  Game/
    GamePhase.swift          phase enum + per-phase timing payload
    GameEngine.swift         @Observable state machine, the heart of it
    DifficultyCurve.swift    all tuning constants
    ScoreKeeper.swift        accrual, multiplier, nerve bonus
    PhoneScreenSim.swift     the mini-apps, as pure functions of elapsed time
  Views/
    RootView.swift           menu / game / game-over routing
    GameView.swift           hold surface + HUD
    PaulView.swift           sprite renderer
    PhoneHandView.swift      the hand + phone overlay shown while holding
    GameOverView.swift       score, submit, retry
    LeaderboardView.swift    GKGameCenterViewController wrapper
  Services/
    LeaderboardService.swift protocol + GameCenter impl + Local impl
    AudioPlayer.swift
    Haptics.swift
  Assets.xcassets
```

### Art

Real pixel art doesn't exist yet, so **Phase 1 ships a programmatic placeholder Paul** drawn with
SwiftUI `Canvas` from a chunky pixel grid. The game is fully playable before any asset
arrives. `PaulView` is the only file that changes when real sprites land.

When sprites do land: `.interpolation(.none)` on every `Image`, or scaled pixel art turns
to mush. Frames needed: back-idle (2), turning (4), facing (2), caught/pointing (1).

The phone prop and its mini-apps are drawn in code on the **same coarse pixel grid** as Paul,
sharing his palette and his 1px outline weight. A shared cell size is the whole trick — it is
what keeps the overlay reading as part of the same artwork rather than a vector UI pasted on
top — so the pixel-art rules above apply to it too.

### Game Center — build behind a protocol

Game Center leaderboards require an App Store Connect app record with a configured
leaderboard ID. **You cannot test submission until that record exists**, and that's an
external dependency on your team's ASC access.

So `LeaderboardService` is a protocol with two implementations: `LocalLeaderboard`
(UserDefaults, works day one) and `GameCenterLeaderboard`. The game is complete and
playable on the local one; Game Center is a swap when ASC is ready.

Note: a client-side timer score is trivially cheatable. For a cohort of mentors who know
each other, that's fine — **we are deliberately building no anti-cheat.**

### Accessibility

This is an accessibility workshop's own app, so it should be exemplary:

- Paul's **body orientation** is the primary signal, with audio and haptic cues alongside —
  never color alone. A colorblind or blind player can play.
- Honor **Reduce Motion**: drop screen shake, keep the turn silhouette readable.
- Full-screen hold target, so 44pt minimums are trivially met.
- Dynamic Type on menu, game-over, and leaderboard.
- **Assist mode**: 1.5x reaction window, separate leaderboard. Also makes live demos safer.

---

## Build phases

0. **Phone overlay** — the hand + phone that rises while you hold, and the two mini-apps it
   plays. Cosmetic, additive, and independent of everything below; it touches no game logic.
1. **Playable loop** — engine, state machine, hold gesture, Canvas Paul, score readout.
   No art, no sound, no network. *Goal: confirm it's fun before building anything else.*
2. **Tune** — difficulty curve, fake-outs, multiplier and nerve bonus. Playtest.
3. **Feel** — audio cues (`AVAudioSession` `.ambient` + `mixWithOthers` so it doesn't kill
   the player's music) and haptics via `.sensoryFeedback`.
4. **Art** — swap real sprites into `PaulView`.
5. **Game Center** — auth, submit, leaderboard UI.
6. **Accessibility pass** — assist mode, Reduce Motion, Dynamic Type, VoiceOver on menus.

Phase 1 is the real risk. If holding-and-releasing doesn't feel good, phases 2–6 are wasted.

---

## Verification

There is no `.xcodeproj` yet, and hand-writing a `project.pbxproj` is fragile. **Fastest
path: create the project in Xcode** (iOS App template, SwiftUI, name `PaulGame`,
minimum iOS 17), then fill in the Swift files.

Then:

1. Run on simulator — but **tune on a real device**. Simulator input latency will lie to
   you about a 0.35s window.
2. Verify by playing: cautious tapping should score low; riding the window should score
   high. If both strategies score similarly, the multiplier needs work.
3. Confirm a fake-out never causes a catch.
4. Toggle Reduce Motion in Settings and confirm the turn is still readable.
5. Play once with the screen off / eyes closed using audio cues only — if that's possible,
   the non-visual signaling is working.
6. Game Center: verify score appears on the leaderboard with a sandbox Apple ID.
