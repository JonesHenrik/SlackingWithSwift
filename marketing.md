# Slacking with Swift — Marketing

> Source material: `plan.md` (the brief), the shipped source in `PaulGame/`, and `findings.md`
> (voice-of-customer research). **Every claim below traces to code that exists today.** Anything the
> research asked for that we don't actually do is listed in *Out of scope* rather than softened into
> a claim.

---

## Positioning

**Who it's for.** Mentors at the Apple Developer Academy in Detroit who trained with Paul Hudson.
Paul has approved use of his likeness as an 8-bit character. It's a party game for a room of people
who know each other and who will absolutely argue about the high score.

**The problem it solves.** The joke it's built on is "don't slack off while working with Claude" —
but the brief makes a deliberate call that shapes all the copy: **this is an honest party game, not
a productivity tool.** It does not monitor your phone usage. It does not pretend to help you focus.
It is a fast reflex game about the in-joke of getting caught slacking. Refusing the wellness-app
framing is a positioning asset, not a limitation — say it out loud.

**The one thing it does brilliantly.** *It makes being careful expensive.*

"Hold as long as you can" isn't a game if letting go early is free — everyone taps and releases
instantly, every run looks the same, and the high score means nothing. So the multiplier climbs
+0.5× per continuous second held and **resets to 1× the moment you let go**, and releasing in the
last 25% of Paul's turn pays a flat +500 bonus. A timid player scores a couple of thousand. Someone
who rides every turn to the last frame scores five to ten times that.

That is the whole pitch: **the score is a measure of nerve, not luck.** Everything else — the exact
detection, the randomized turns, the escalation — exists so that sentence is true.

---

## Proof

The complaints below are the ones Slacking with Swift genuinely answers. Quoted verbatim.

### 1. "I didn't move and I still died" — the genre's defining failure

> **"It kills you when you didn't even move. I was doing great then it went red light. I didn't move and I still got shot that happens to a lot a players. Like 10 people die at once when not a single one of them moved."**
> — *dk what 2 put lol*, 1★, [Red Light Green Light Pro](https://apps.apple.com/us/app/red-light-green-light-pro/id1589204209?see-all=reviews&platform=iphone)

> **"Every time it says red light I stop but it kills me Anyway and when I diy a stupid add comes on every single time"**
> — *Nate_2O1O*, 1★, review titled **"Cheats"**, [Red Light Green Light Pro](https://apps.apple.com/us/app/red-light-green-light-pro/id1589204209?see-all=reviews&platform=iphone)

> **"ok so i wasnt moving and i got killed sooo yeah"**
> — *preppylorax22*, [itch.io](https://nstefan.itch.io/squid-game-online-red-light-green-light/comments)

**How Slacking with Swift answers it:** there are exactly two ways to be caught, both of them events, neither of
them a guess — you were still holding when Paul finished turning, or you put your finger down while
he was already looking. Nothing polls, nothing samples, nothing drifts, so "I let go in time" and
"the game says I didn't" cannot disagree.

### 2. "I stopped at red light and died anyway" — no visible grace window

> **"The detection is a little awkward…I started running when the light was green and got shot while a lot of npcs will run during red light and not get shot"**
> — *SabreDorko*, [itch.io](https://nstefan.itch.io/squid-game-online-red-light-green-light/comments)

**How Slacking with Swift answers it:** Paul's turn *is* the grace window, and it's drawn on screen. The moment
he starts turning, the status card reads **LET GO** and a bar drains showing exactly how much time is
left — 0.9 seconds early on, tightening to 0.35 at full difficulty. You can release at any point
before it empties. Releasing at the last moment is rewarded, not punished.

### 3. "It always reacts in a pattern"

> **"And the red light green light always reacts in a pattern… please don't put the colors in a pattern."**
> — *Choclate Donut🍩*, 1★, [Red Light Green Light](https://apps.apple.com/us/app/red-light-green-light/id1470921227?see-all=reviews&platform=iphone)

**How Slacking with Swift answers it:** every phase length is drawn at random inside a range — how long his back
is turned, how long he stares, and whether he fakes you out with a twitch that never becomes a turn.
There is no sequence to memorise.

### 4. "It's literally the same thing over and over again"

> **"Upon finishing Round 2, I was immediately apparent that all the levels were simply repeating…It's literally the same thing over and over again…No increase in difficulty at all"**
> — *Rock4Jesus777*, [K-Games Challenge](https://apps.apple.com/us/app/k-games-challenge/id1587644107?see-all=reviews&platform=ipad)

**How Slacking with Swift answers it:** difficulty ramps continuously over the first twenty turns. His turn
speeds up from 0.9s to 0.35s, his back is turned for less and less time, and the chance he fakes you
out climbs from zero to roughly one in three. The pressure comes from Paul himself, not from levels.

### 5. Ads — and especially ads that kill you

> **"There's so many ads that I can't even play a single challenge without getting an ad in the middle of the challenge…the challenge literally continues in the background while I watch the ad and I'm dead by the time the ad is over."**
> — *Heythereimkayla*, titled **"Too many ads"**, [K-Games Challenge](https://apps.apple.com/us/app/k-games-challenge/id1587644107?see-all=reviews&platform=ipad)

> **"One of the worst games I ever played. first off, the amount of advertisements are in this game is bad enough but you can't skip the for more than 30 seconds?!"**
> — *Greenscreen Bucko*, [Red Light Green Light 3D Fun, Google Play](https://play.google.com/store/apps/details?id=com.jamboStudio.RedLightGreenLight3DFun&hl=en_US)

**How Slacking with Swift answers it:** there are no ads. Not fewer ads, not skippable ads — none. There's also
no IAP, no account, and no network call of any kind. Nothing can interrupt a run because there is
nothing in the app capable of interrupting one.

### 6. "I didn't know it was a hold"

> **"the instructions were not that clear i have to hold forward and not tap"**
> — *riot_grrl*, [itch.io](https://nstefan.itch.io/squid-game-online-red-light-green-light/comments)

**How Slacking with Swift answers it:** the screen says **HOLD TO WORK / Press and hold anywhere to start
earning** before you've done anything, and once you're playing it states your status live —
**HOLDING — EARNING** or **NOT HOLDING — NO POINTS** — so the input model is never ambiguous. The
whole screen is the button, and there's no tapping or shaking anywhere in the game.

---

## Voice

**How we should sound.** Modelled on how people write when they actually like one of these games:

> **"people are saying that there is way to many ads witches they are wrong because literally there is no ads"**
> — *Chayita13*, 5★, [Red Light Green Light](https://apps.apple.com/us/app/red-light-green-light/id1470921227?see-all=reviews&platform=iphone)

> **"I deleted it a couple times just because it was getting boring. I got it back though just so I could have something to do."**
> — *mogn34!*, 3★, [Red Light Green Light](https://apps.apple.com/us/app/red-light-green-light/id1470921227?see-all=reviews&platform=iphone)

What that voice has in common, and what we should copy:

- **Short, flat sentences.** No adjective stacks. "There are no ads" beats "a refreshingly clean,
  ad-light experience."
- **Concrete and checkable.** People praise numbers and specifics — *no ads*, *the graphics*. Every
  claim we make should be one a player can verify in thirty seconds.
- **Define ourselves by what we don't do to you.** The warmest reviews in this genre are relief that
  the game isn't hostile. Lead with no ads, no accounts, no interruptions.
- **Say the joke plainly, don't explain it.** It's a party game for people who know Paul. It doesn't
  need a mission statement.
- **Never pre-blame the player.** The #1 complaint in the genre is people being told their reflexes
  failed when they believe the detector did.

**Sentences we should never write.** Each of these is a promise a rival made that players publicly
called out:

1. > ❌ *"Endless levels and non-stop new challenges!"*

   Killed by: **"It's literally the same thing over and over again…No increase in difficulty at
   all"** — *Rock4Jesus777*. We have one loop and honest escalation. Say *that*: "It gets faster
   until it beats you." Never imply content volume we don't have.

2. > ❌ *"Free to play — jump in now!"*

   Killed by: **"Way too many ads"** — *rennau's lady*, 1★, and **"The game is good i like it but
   too much adds."** — *Sonu Nimble*. "Free" has been trained to mean ad-funded. We say **"No ads.
   No purchases."** — the specific claim, not the word that's been poisoned.

3. > ❌ *"Test your reflexes — only the fastest survive!"*

   Killed by: **"I didn't move and I still got shot"** — *dk what 2 put lol*, and the review simply
   titled **"Cheats"**. Copy that puts the outcome on the player's reflexes reads as pre-emptive
   blame in this genre. Describe the mechanic, not the player's inadequacy.

---

## Out of scope

Things the research asked for that we should **not** market, because the app doesn't do them. Listed
so nobody writes a claim we can't back.

| Research asked for | Reality |
|---|---|
| "there's no sound" — audio as a feature | **No audio at all.** It's a planned phase. Don't mention sound. |
| A "yellow light" partial-risk tier | Not built. The fake-out is a *safe* twitch, not a risk tier — don't conflate them. |
| Play as the light-caller ("be the next person to control the lights") | Not built. Single-player only. |
| Lobbies / "play against each other" | No multiplayer, no network. |
| Skins, currency, unlockables | None. Nothing to earn or spend. |
| A death screen showing *why* you were caught | **We show score and turns survived — not the moment of detection.** The research specifically recommended "you were still holding 0.3s after he turned." We don't do it, so don't claim it. Strong candidate to build. |
| Leaderboards / ranks | Only a single local best score on the device. No Game Center, no online board yet — don't say "leaderboard." |
| "The screen needs to be bigger!" (iPad) | Layout is untested on iPad. Make no tablet claims. |
| "i cant retry it by clicking the retry button" | The AGAIN button exists but **its restart path has not been verified.** Don't market fast restart until someone taps it on a device. |
| "Don't take away what I earned" (rank loss) | Best score persists, but backgrounding the app **discards the run in progress**. Don't make durability promises. |
| Ad-free as a paid upgrade | There's nothing to remove and nothing to sell. Frame as "no ads," never "remove ads." |

**One caution on Proof #1.** Our detection genuinely is exact, but "fair detection!" is precisely the
claim rival apps made and players rejected. Don't assert fairness as an adjective — describe the
mechanism ("you can let go any time before he finishes turning; the bar shows how long you have")
and let players verify it themselves. Specificity is what makes the claim survive contact with a
genre that has been lied to.
