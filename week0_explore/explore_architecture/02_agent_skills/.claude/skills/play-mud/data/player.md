# Player: dummy

Last updated: 2026-07-18 (session 2, end)

This file is the character's state, goals, and lessons learned. Map facts,
shop prices, and mob stats belong in world.md instead — cross-reference
rather than repeating numbers here, since numbers copied into two files
drift out of sync with each other (this happened once already: an exp
count went stale in one section while another section moved on).

## Goals
Check these first thing every session and let them drive what you do if
the user hasn't given you something more specific to do right now. Don't
restate numbers here — see "Current status" below for the live snapshot.

- [ ] Defeat: the massive minotaur, said to be in the newbie zone north of
      Midgaard (**primary goal**, set 2026-07-18). Not yet located — see
      world.md "North of Midgaard" for what's mapped so far. Likely behind
      one of the maze's closed doors or the pitch-black room.
- [ ] Reach level 7 (**supporting goal** — the character needs to survive
      several levels of grinding before the minotaur is safely fightable).
      Per `levels 7`: level 2 = 2000 exp, level 7 = 64,000 exp. This is a
      genuinely long grind across many sessions, not something close.

Check a box (`[x]`) instead of deleting the line when a goal is completed,
and add a dated Session Log note about how it was done.

## Current status
The one place numeric character state lives. Refresh from `score` early
in a session — combat and rest ticks happen on the MUD's own clock, so a
number written down mid-session can already be stale by the time you read
it back.

- Level / title: 1, "Dummy the Swordpupil"
- Class: Warrior (fighter) — skills are kick, rescue, track, bash
- HP / Mana / Move: 11(20) / 100(100) / 57(85) — resting at The Dirty
  Hallway (newbie zone maze)
- Location: The Dirty Hallway
- Gold / questpoints: 0 carried, **7 banked at the ATM** (torch purchase
  in progress — dagger already bought, see equipment below)
- Exp: 368/2000 toward level 2
- Practice sessions remaining: 0 (started at 2, both spent on kick;
  more arrive on level up, along with rescue/track/bash unlocking)
- Hunger/thirst: hungry, not thirsty (see world.md Points of Interest for
  the free fountain; eating any meat from a kill clears hunger)
- `wimpy` set to 5 (auto-flees combat below 5 HP, lowered by the user
  from 10 — see Hazards)

## Learned skills & spells
Proficiency words the game reports (e.g. "not learned", "bad", "awful",
"poor", ... up to "superb") — check before spending a practice session on
something already learned well.

- kick: poor (raised from bad — 2nd practice session spent here)
- rescue / track / bash: **not available yet** — `practice bash` gave
  "You do not know of that skill," and `practice` (no args) only lists
  kick as a known skill. These are likely level-gated, not just
  unlearned; another reason leveling up matters beyond raw HP/damage.

## Notable inventory & equipment
- **Dagger** (wielded) — bought 2026-07-18 for 13g, our first weapon.
  **Confirmed big upgrade**: first fido with it went from full HP to
  "mortally wounded" to dead while we stayed at 85% HP the whole fight —
  night and day versus bare-handed fights that regularly dragged us to
  40-70% HP for the same kill (or no kill at all). The 70% flee threshold
  was tuned for unarmed combat and may now be overly conservative with a
  weapon equipped — worth revisiting after more data, but err cautious
  until then.
- Still no armor or light source (see Money problem — 16g torch is next).
- **A janitor NPC steals corpses, not decay timing** — the actual cause
  behind several missed loots: `read` showed "The janitor gets the
  corpse of the beastly fido. The janitor leaves south." Janitors wander
  the same rooms fidos do (Market Square, Common Square, Main Street
  junctions), and they can grab a corpse faster than we can react even
  going straight for `get all corpse` with no `look` in between. Losing
  this race is common, not a mistake to fix by being faster. Given that,
  don't treat every fight as a gold attempt — it's fine to chain fido
  kills purely for exp and only bank whatever loot happens to survive the
  janitor, rather than pausing to fight the theft.

## Hazards — read before fighting anything
Rules learned the hard way. Died twice this session; both are folded in
here rather than re-told in the session log below.

- **Guards defend "harmless" town mobs.** Landing a killing blow on a
  fido in a room with a Peacekeeper/cityguard draws the guard into
  attacking you too, and the guard hits far harder than the fido did —
  went from ~78% HP to dead in ~5 rounds. Guards don't intervene in
  non-lethal fido fights, only once one actually dies. See world.md for
  which rooms have guards; the newbie zone maze has none.
- **Combat runs in real time, independent of when we poll — this has
  killed us twice.** The MUD keeps simulating rounds on its own clock
  whether or not commands are being sent, so any latency between `score`
  checks can burn through a safety margin before we ever see it. Three
  layers of defense, all active: (1) never step away or pause mid-fight
  without fleeing first, (2) manually flee at 70% of max HP (raised from
  an initial 40-45% after a death at that lower threshold), (3) `toggle
  wimpy <#hp>` as a hard auto-flee floor, capped at half of current max HP
  (lowered by the user from 10 to 5 at 20 max HP — a true last-resort
  catch well below our normal 70% manual flee point, not a replacement
  for it). It has already triggered for real once at the old 10 setting.
  Wimpy is a backstop, not a replacement for judgment — e.g. it can't tell
  the difference between real danger and finishing off an incapacitated
  enemy (see below).
- **Fleeing costs exp** (confirmed: dropped from 52 to 45 after one flee,
  no death involved) — so fleeing isn't free even when it's the right
  call safety-wise.
- **Watch the enemy's status messages, not just our own HP.** Fled once
  right as the opponent hit "is incapacitated and will slowly die, if not
  aided" — i.e. it was already a near-certain kill, and fleeing threw that
  away plus ate the exp penalty for no safety benefit. If the enemy is
  stunned/incapacitated and our own HP is still reasonably safe (comfortably
  above the hard floor, not just at the flee line), finishing it off beats
  fleeing on autopilot.
- Also: **guards patrol between rooms, they aren't fixed to one location**
  (watched a Peacekeeper leave a room on its own). A room being guard-free
  a moment ago doesn't mean it stays that way — check with `look` right
  before landing a killing blow, not just once at the start.
- **Bank gold immediately after every kill.** Any ATM (Temple Of Midgaard,
  Guild of Swordsmen entrance hall, others) takes `deposit <amount>` and
  `balance`. Since death wipes carried gold (see above), banked gold
  should be safe from that — deposit before doing anything else risky,
  not just before logging off.
- **A wounded/mortally-wounded mob left over from someone or something
  else is a near-free kill** — fled from one fight straight into a
  different room where an already "mortally wounded" fido was lying,
  finished it in one hit for a clean kill with barely any risk. Worth
  checking room contents for this after any flee, not just moving past.
- **Max HP comes from leveling up, scaled by Constitution** (`help
  constitution`: "Determines how many hit points you gain per level, and
  how well you heal"). Found no way to raise Constitution directly as a
  mortal — no potion, item, or trainer for it; the `SET` command that
  changes stats is immortal-only. So combat/exp-grinding toward a level
  isn't just "the current strategy," it appears to be the *only* lever
  we have for more HP — no shortcuts found.
- **Verify the exact target name with `look` before `kill` when multiple
  mobs share a room.** `kill guard` or a partial name can mis-target a
  different mob present (accidentally fought a "creepy crawler" instead
  of the intended "Newbie Guard" this way).
- **Idle timeout disconnects with no penalty** — unlike death, sitting
  idle too long gets the connection dropped ("pulled into a void" then
  "Multiple login detected"), but reconnecting and logging back in
  restored gold/exp exactly as they were. Annoying but harmless; `toggle
  wimpy` and other settings (confirmed: wimpy) persist across it too.
- **Death mechanics**: HP goes negative -> "incapacitated, will slowly
  die" -> connection drops to the OOC menu -> choosing "1) Enter the
  game" respawns at The Temple Of Midgaard with 1 HP, full mana/move.
  **All carried gold is lost** on death (confirmed twice); exp also takes
  a penalty (dropped from a peak of ~92 to 82 the second time). No
  inventory was lost either time, but that's untested with actual items
  in hand — assume everything carried is at risk and avoid banking a
  large stash before a fight.
- **Thirst visibly stalls HP regen** — resting while thirsty can keep HP
  flat for many ticks in a row; drinking (free, see world.md fountain
  entry) unstalls it almost immediately. Always clear thirst before
  relying on rest to heal.

## Money problem
Character started with **0 gold** and no equipment (see world.md for shop
prices — cheapest weapon and cheapest food both cost more than 0). Killing
a mob for loot is the only income found so far; see Hazards above for why
that's riskier than it sounds, and for how to bank it safely once earned.
Ruled out as free income sources (exhaustively checked every shop/NPC in
town for `quest list`, plus the Post Office, the Grunting Boar Inn's bar
and Cryogenic Center, the Grubby Inn, and begging): the Midgaard Donation
Room (empty, NPC doesn't respond to requests), the autoquest system (no
questmaster found anywhere in town), and simple begging (`beg` is just a
joke emote). **Dagger bought** (13g, see equipment below) — see Current
Status above for the live banked-gold figure. The 16g torch at the
General Store (a light source for the maze's dark room) is next, but
deprioritized by the user for now in favor of more exp grinding.

## Session log
Newest first. Keep entries short — a line or two per session — and point
back to the Hazards/Known Mobs sections instead of re-explaining a lesson
that's already written down there. **Within one continuous session, edit
that session's entry in place rather than appending a new "part N" entry
each time memory is saved** — the log is a breadcrumb trail across
sessions, not a blow-by-blow transcript; let Hazards/Known Mobs carry the
mechanics and keep this to what happened and what's next.

- 2026-07-18 (session 2): Set the primary goal (defeat the massive
  minotaur, reach level 7) and mapped the newbie zone maze north of
  Midgaard (see world.md). Died three times — a Peacekeeper defending a
  killed fido, an unmonitored Newbie Guard fight, and a plain fido fight
  that exposed the real-time-combat-clock risk — each drove a Hazards
  rule (guard risk, never leave combat unmonitored, flee threshold raised
  45%→70%, `wimpy` set to 10, later lowered to 5 by the user as a
  last-resort backstop). Also survived an idle-timeout disconnect with no
  penalty (unlike death — gold/exp were untouched on reconnect). Bought
  and equipped a dagger (13g) — confirmed a major upgrade against fido
  specifically, less so against Newbie Guard/newbie monster. Banked gold
  via ATM after kills rather than carrying it. Ruled out every free-income
  avenue in town (Money problem). Learned level 7 needs 64,000 exp — a
  genuinely long multi-session grind, and that Constitution (fixed, no
  way to raise it as a mortal) is the only lever for more max HP besides
  leveling. Newbie monster proved a consistently bad matchup (0-for-2)
  and is now deprioritized below fido; Newbie Guard is mixed (one clean
  win, one costly flee). Fidos were repeatedly scarce in town this
  session (heavy guard patrols), forcing fallback to the maze more than
  intended. User flagged a possible "red room" minotaur location in the
  maze — still unconfirmed. Ended at 368/2000 exp, level 1, dagger
  equipped, resting in the maze, hungry (see Current Status for exact
  gold/HP). **Next**: prefer fido hunting
  over newbie-zone mobs when available, buy the torch (16g, deprioritized
  for now) once banked, keep searching the maze's remaining closed
  doors/dark room/red room for the minotaur once stronger.
