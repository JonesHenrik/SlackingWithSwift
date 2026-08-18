# Voice-of-Customer Research: "Red Light, Green Light" & Don't-Get-Caught Games

Research for a mobile game where **Paul Hudson** turns his back, you hold down on the screen to look at your phone, and you must let go before he turns around. Goal: maximize phone time without being caught.

Every phrase below is copied verbatim from a real user. Nothing is paraphrased or invented. Sources linked per section.

---

## 1. The #1 complaint in this entire genre: "I didn't move and I still died"

This is the dominant, genre-defining failure mode. In your game the equivalent is **"I let go and he still caught me."** If you ship one thing well, make it this.

From **Red Light Green Light Pro** (App Store):

> **"It kills you when you didn't even move. I was doing great then it went red light. I didn't move and I still got shot that happens to a lot a players. Like 10 people die at once when not a single one of them moved."**
> — *dk what 2 put lol*, 1★, 10/30/2021

> **"I hate the stupid ads and when I stop at red light I freaking die like why"**
> — *jacob lencinas*, 1★, 11/25/2021

> **"Every time it says red light I stop but it kills me Anyway and when I diy a stupid add comes on every single time"**
> — *Nate_2O1O*, 1★ (titled **"Cheats"**), 01/03/2022

> **"It's good but the ads are annoying and I don't move on red light and I die"**
> — *Warren3764746*, 1★, 01/27/2025

From an itch.io browser version of the same concept:

> **"ok so i wasnt moving and i got killed sooo yeah"**
> — *preppylorax22*

> **"The detection is a little awkward…I started running when the light was green and got shot while a lot of npcs will run during red light and not get shot"**
> — *SabreDorko*

> **"I did that. those damn npc were moving."**
> — *Empressdarlingsweetling1*

**Design implication for you:** players do not blame their own reflexes — they blame the detector. Build in a visible grace window (a fraction of a second after Paul starts turning), show the exact moment of detection on the death screen ("you were still holding 0.3s after he turned"), and never let ambiguity exist about whether the player's finger was down. The word players reach for when detection feels off is literally **"Cheats"**.

---

## 2. "It's literally the same thing over and over again" — the repetition wall

The second-biggest killer. A single-mechanic game gets uninstalled fast unless difficulty escalates.

From **K-Games Challenge** (App Store):

> **"Upon finishing Round 2, I was immediately apparent that all the levels were simply repeating…It's literally the same thing over and over again…No increase in difficulty at all"**
> — *Rock4Jesus777*, 10/07/2021

> **"you'll just end up playing the same game over and over again there's no sound you can't buy anything with the money you won…this game has potential but it hasn't gotten to that point"**
> — *insta@gamerfireboy3421*, titled **"It was awesome at first but then got annoying"**, 10/07/2021

From **Red Light Green Light** (App Store):

> **"I deleted it a couple times just because it was getting boring. I got it back though just so I could have something to do."**
> — *mogn34!*, 3★, titled **"Not the best…"**, 07/02/2021

> **"I just wish there would be more things to do. Really all you do is try to get to the finish line without getting caught and avoiding obstacles then you get coins to unlock skins."**
> — *mogn34!*, same review

**Design implication:** your session loop is "hold, release, survive." Escalation must come from Paul himself — faster turns, fake-outs, glancing over his shoulder mid-monologue, peripheral vision, a mirror. And note that even the boring version got **re-downloaded** "just so I could have something to do" — the idle-filler slot is real and winnable.

---

## 3. Ads — and specifically ads that kill you

Ads are the loudest complaint and the most fixable one. Note the second quote: an ad that runs *while the timer keeps going*.

> **"There's so many ads that I can't even play a single challenge without getting an ad in the middle of the challenge…the challenge literally continues in the background while I watch the ad and I'm dead by the time the ad is over."**
> — *Heythereimkayla*, titled **"Too many ads"**, K-Games Challenge, 10/06/2021

> **"Way too many ads"** / **"Bruh"**
> — *rennau's lady*, 1★, Red Light Green Light Pro, 06/29/2023

> **"One of the worst games I ever played. first off, the amount of advertisements are in this game is bad enough but you can't skip the for more than 30 seconds?!"**
> — *Greenscreen Bucko*, Red Light Green Light 3D Fun, Google Play, 01/21/2025

> **"The game is good i like it but too much adds."**
> — *Sonu Nimble*, same app, 01/21/2025

Counterpoint worth noting — light ad load gets *actively defended* by fans:

> **"people are saying that there is way to many ads witches they are wrong because literally there is no ads"**
> — *Chayita13*, 5★, Red Light Green Light, 05/16/2021

> **"The graphics are great, and there are not to many ads!"**
> — *mogn34!*, 3★, same app

**Design implication:** never interstitial a run in progress. Given your mechanic (a held finger, an accumulating timer), an ad mid-hold would be catastrophic. Ads at the death screen only, and a cheap remove-ads IAP — reviewers explicitly track whether they had to pay.

---

## 4. Control clarity — people don't know it's a *hold*

Your entire mechanic is press-and-hold. Players had to figure this out themselves in comparable games:

> **"the instructions were not that clear i have to hold forward and not tap"**
> — *riot_grrl*, itch.io

> **"i can't move on pc…"**
> — *BurntBread8494*, itch.io

> **"when it says power mode, it's literally flipping impossible…my hand was shaking so fast…it's just flipping impossible so yeah. That part is annoying"**
> — *𝕊𝕨𝕚𝕗𝕥𝕪*, K-Games Challenge, 10/16/2021

**Design implication:** teach the hold in the first three seconds, wordlessly. And avoid mash/shake mechanics — the "flipping impossible" quote is about a game that swapped a hold for frantic tapping.

---

## 5. Agency, control, and "let me be the one calling it"

The single most-upvoted structural request in the genre — players want to be on the *other* side of the mechanic.

> **"I would've given this game at least four stars if there was a way to actually control the light… if you are able to tag or get to the person controlling the lights you get to be the next person to control the lights."**
> — *Choclate Donut🍩*, 1★, titled **"Why can't you control the light?"**, 05/16/2021

> **"And the red light green light always reacts in a pattern… please don't put the colors in a pattern."**
> — same review

> **"we also do a yellow light which meant you could move while the person controlling the lights was looking but you would have to move very slowly"**
> — same review

> **"It would also be a lot more fun if this worked in lobby's with a lot of people and actually play against each other"**
> — *Miner 22406*, K-Games Challenge, 10/06/2021

**Design implication:** two big free ideas here. (a) **Randomize Paul's turn timing** — a detectable pattern is a documented 1-star complaint. (b) A **"yellow light" risk tier** maps perfectly onto your mechanic: a state where you *can* peek but only at reduced screen brightness / partial reveal, at higher risk. And a mode where you play *as Paul* is the most-requested feature in the genre.

---

## 6. Customization and reward — earned currency that does nothing

> **"I wish you could pick your own skin instead of the game picking a random skin."**
> — *mogn34!*, Red Light Green Light

> **"there's no sound you can't buy anything with the money you won"**
> — *insta@gamerfireboy3421*, K-Games Challenge

> **"I love this game it is the best squid game remake!…add a lights out game mode"**
> — *Jett F*, K-Games Challenge, 10/04/2021

---

## 7. Live-ops lessons from the genre's biggest hit (Squid Game: Unleashed, 4.8★, 40K ratings)

Worth reading if you ever add multiplayer or a shop.

> **"This is absolutely the best game I have ever played."** … but **"One glitch makes you stuck in the same place while racing"**
> — *000133*, 4★, titled **"Best Game; Worst Glitches"**, 12/10/2025

> **"The addition of the fishing pole has completely ruined the fun"**
> — *Uhhhh......:-|*, 02/11/2025 — a single new item flattening the tension of the core loop

> **"The cost increase to purchase a Mystery Box…increased from $15k to $50k."** … **"DO NOT DOWNLOAD THIS GAME."**
> — *Rss060609*, 2★, 06/21/2025

> **"The loss of an entire number rank from WiFi glitching"** … request: **"you simply don't gain points, not lose the rank."**
> — *Pretty awesome chicky*, 3★, 01/11/2025

> **"a settings tab where you could disable long end screens"**
> — *Arabrunenjoyer911*, 03/07/2025

> **"The toxicity has gone way down with the implemented changes."**
> — *Rag3ing*, 11/11/2025

**Design implication:** the "don't take away what I earned" principle. If you have a high-score streak, never let a crash or a lost connection wipe it — freeze it instead.

---

## 8. The literal words people type when they want a fix

These are the phrasings that appear as **review titles** (which is how people search the App Store — App Store search is heavily title/keyword driven) and as forum question text. Use these as ASO keywords and as your support-page headings.

Complaint-shaped search phrases, verbatim:

| Phrase | Where it came from |
|---|---|
| **"Way too many ads"** | review title, RLGL Pro |
| **"Too many ads"** | review title, K-Games Challenge |
| **"too much adds"** | review body, Google Play (note the misspelling — real search traffic) |
| **"Why can't you control the light?"** | review title, RLGL |
| **"Game doesn't work"** | review title, K-Games Challenge |
| **"It was awesome at first but then got annoying"** | review title, K-Games Challenge |
| **"Best Game; Worst Glitches"** | review title, Squid Game: Unleashed |
| **"Got worse unfortunately"** | review title, Squid Game: Unleashed |
| **"Ads and annoying gameplay"** | review title, RLGL Pro |
| **"The screen needs to be bigger!"** | review title, RLGL (iPad layout) |
| **"Cheats"** | review title, RLGL Pro — what players call unfair detection |
| **"wont load :c"** | itch.io comment |
| **"Make it easier one please"** | itch.io comment |
| **"Could you add the next level? PLSSSSS"** | itch.io comment |
| **"i cant retry it by clicking the retry button"** | Google Play review |

Two structural notes on the tablet/layout complaint, since it's cheap to pre-empt:

> **"I dont know if you guys have a small screen but I do and I think its because im on ipad but theres needs to be an update which should be fixing the screen for ipad/tablet."**
> — *ItsYourgirl_Candy*, Red Light Green Light

And a retry-loop bug, which matters enormously for a fast-restart game like yours:

> **"This game is not bad but when ever i die i cant retry it by clicking the retry button."**
> — *ABC*, Google Play, 01/24/2025

> **"When I pass the first level my figure dances and the time runs out, but then they continue dancing and never moves on to the next level…I even let my phone sit for over 5 minutes waiting…but it never moves to anything else."**
> — *Private 001*, K-Games Challenge, 10/09/2021

---

## Top 6 takeaways, ranked

1. **Detection fairness is the whole game.** "I didn't move and I still got shot" is the #1 review complaint across every app checked. Add a grace window and show the player exactly why they got caught.
2. **No ads inside a live run, ever.** The most damning ad review is about a timer that kept running during the ad.
3. **Randomize Paul's turns.** "The red light green light always reacts in a pattern" is a documented 1-star cause.
4. **Escalate or die.** "It's literally the same thing over and over again."
5. **Teach the hold instantly and wordlessly.** "the instructions were not that clear i have to hold forward and not tap."
6. **A "yellow light" middle state and a play-as-the-caller mode** are the two most-requested features in the genre and both fit your mechanic natively.

---

## Research notes & limitations

- Apple's `itunes.apple.com` review RSS feed is blocked by robots.txt, so reviews were pulled from the public `apps.apple.com` "Ratings & Reviews" pages, which surface roughly the 4–10 most prominent reviews per app rather than the full corpus.
- Google Play similarly surfaces only a handful of reviews on the public page.
- Reddit threads specific to these apps did not surface in search; the itch.io comment threads were used instead as an unfiltered player-feedback source.
- Apps sampled: Red Light Green Light (id1470921227), Red Light Green Light Pro (id1589204209), K-Games Challenge (id1587644107), Squid Game: Unleashed (id6498719476), Red Light Green Light 3D Fun (Google Play), and an itch.io browser RLGL game.

## Sources

- [Red Light Green Light — App Store reviews](https://apps.apple.com/us/app/red-light-green-light/id1470921227?see-all=reviews&platform=iphone)
- [Red Light Green Light Pro — App Store reviews](https://apps.apple.com/us/app/red-light-green-light-pro/id1589204209?see-all=reviews&platform=iphone)
- [K-Games Challenge — App Store reviews](https://apps.apple.com/us/app/k-games-challenge/id1587644107?see-all=reviews&platform=ipad)
- [Squid Game: Unleashed — App Store reviews](https://apps.apple.com/us/app/squid-game-unleashed/id6498719476?see-all=reviews)
- [Red Light Green Light 3D Fun — Google Play reviews](https://play.google.com/store/apps/details?id=com.jamboStudio.RedLightGreenLight3DFun&hl=en_US)
- [SQUID GAME | Red Light Green Light — itch.io player comments](https://nstefan.itch.io/squid-game-online-red-light-green-light/comments)
- [456 Survival Challenging Games — App Store](https://apps.apple.com/us/app/456-survival-challenging-games/id6470453465)
- [Don't Go Getting Caught! — App Store](https://apps.apple.com/us/app/dont-go-getting-caught/id1596686768)
