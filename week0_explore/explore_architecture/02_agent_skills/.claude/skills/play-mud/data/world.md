# World map

Accumulated map knowledge for this MUD, built up across sessions so you
don't have to rediscover rooms, guild entrances, and mobs by wandering
every time. This is the stock tbaMUD "City of Midgaard" starting area.

This file owns objective facts: room layout, shop prices, NPC/mob
locations and stats. Character-specific state, goals, and lessons learned
belong in player.md instead — if you're about to write down a reason
*why* something matters to the player, that probably belongs there, with
just a fact and a pointer left here.

**Mob combat data lives only in the "Known Mobs" section below** — not
in individual room entries. A room's "Notable" line should name what's
there and point to Known Mobs, not repeat fight details; repeating them
in both places is exactly how this file drifted out of sync with itself
last time (a mob's fight outcome was updated in one spot but not the
other). The "North of Midgaard" route and "Guild / practice locations"
summaries below are a deliberate exception — they're compact turn-by-turn
shortcuts, cheap to keep even though the same path is technically
derivable by chaining individual rooms' exits.

Format for each room:
```
### <Room Name>
- Exits: n -> <dest or "unexplored">, s -> <dest>, ...
- Notable: shops, guildmasters, mobs (name only, see Known Mobs), hazards
```

## Rooms — Midgaard city

### The Bakery (character start point)
- Exits: s -> Main Street (Armory jct)
- Notable: baker NPC, buy/list bread & pastry (prices under Points of
  Interest)

### Main Street (Armory jct)
- Exits: n -> The Bakery, s -> The Armory, e -> Market Square

### The Armory
- Exits: n -> Main Street (Armory jct)
- Notable: armorer NPC sells armor; dead end

### Market Square
- Exits: n -> Temple Square, s -> Common Square, e -> Main Street (Pet
  Shop jct), w -> Main Street (Armory jct)
- Notable: central hub; Peacekeeper/cityguard present — see Known Mobs
  "Fido" entry for why that matters; Mayor NPC wanders through

### Temple Square
- Exits: n -> Temple Of Midgaard, e -> Grunting Boar Inn (unexplored
  interior), s -> Market Square, w -> Clerics' Guild (unexplored interior)
- Notable: free fountain (see Points of Interest); ATM one room north

### The Temple Of Midgaard
- Exits: n -> By The Temple Altar, e -> Midgaard Donation Room, s/d ->
  Temple Square, w -> Reading Room (unexplored)
- Notable: ATM in the wall; this is the death-recall room

### Midgaard Donation Room
- Exits: w -> The Temple Of Midgaard
- Notable: empty drop-off spot for player-donated items; resident NPC
  ("a kind soul") doesn't respond to requests for help — not a source of
  starting funds

### By The Temple Altar
- Exits: n -> leads out the back toward the countryside, s -> The Temple
  Of Midgaard
- Notable: dead-end-ish shrine room, statue of Odin

### Common Square
- Exits: n -> Market Square, e -> Dark Alley, s -> The Dump, w -> Poor
  Alley
- Notable: fidos reliably seen here; **guarded by a Peacekeeper** — see
  Known Mobs "Fido" entry before fighting anything here

### The Dump
- Exits: n -> Common Square, d -> sewer system (unexplored)
- Notable: garbage/sewer entrance; darkness varies with an in-game
  day/night cycle (watch for "The day has begun")

### Poor Alley (west end, by the wall)
- Exits: e -> The Eastern End Of Poor Alley, w -> Wall Road (mid)
- Notable: a green gelatinous blob and a beggar seen here — blob
  unconsidered, treat with caution

### The Eastern End Of Poor Alley
- Exits: e -> Common Square, s -> Grubby Inn (unexplored interior), w ->
  Poor Alley

### Dark Alley
- Exits: w -> Common Square, s -> Guild of Thieves (unexplored interior,
  not our guild), e -> The Dark Alley At The Levee
- Notable: a mercenary NPC waiting for a job here

### The Dark Alley At The Levee
- Exits: e -> unexplored, s -> the levee (unexplored), w -> Dark Alley

### Main Street (Pet Shop jct)
- Exits: n -> The General Store, e -> Main Street (weapon shop jct), s ->
  The Pet Shop, w -> Market Square
- Notable: Peacekeeper present

### The General Store
- Exits: s -> Main Street (Pet Shop jct)
- Notable: grocer NPC; dead end

### The Pet Shop
- Exits: n -> Main Street (Pet Shop jct)
- Notable: Pet Shop Boy NPC; dead end

### Main Street (weapon shop / Guild of Swordsmen jct)
- Exits: n -> The Weapon Shop, s -> Guild of Swordsmen entrance, e ->
  Inside The East Gate Of Midgaard, w -> Main Street (Pet Shop jct)
- Notable: warrior guild junction; fidos loiter here

### Inside The East Gate Of Midgaard
- Exits: e -> Outside The East Gate Of Midgaard, s -> Ye Olde Water
  Shoppe, w -> Main Street (weapon shop jct)
- Notable: heavily guarded (5 cityguards seen at once, plus a Peacekeeper)

### Ye Olde Water Shoppe
- Exits: n -> Inside The East Gate Of Midgaard
- Notable: Wally the Watermaster sells water — cup 2g, bottle 12g,
  canteen 57g. Cheaper than the Temple Square fountain trip if we're
  already out this way, but the fountain is free, so no real reason to
  spend gold here unless it's more convenient in the moment.

### Outside The East Gate Of Midgaard
- Exits: e -> The City Entrance (a different, higher-level zone — see
  below), w -> Inside The East Gate Of Midgaard

### The City Entrance
- **This zone is above your recommended level** (the game says so
  explicitly on entry) — leads east into a forest zone. Turned back
  immediately; do not grind here at level 1.

### The Weapon Shop
- Exits: s -> Main Street (weapon shop jct)
- Notable: weaponsmith NPC. Prices: dagger 13g, wooden club 16g, small
  sword 83g, warhammer 69g, long sword 835g, flail 870g

### The Entrance Hall To The Guild Of Swordsmen
- Exits: n -> Main Street (weapon shop jct), e -> The Bar Of Swordsmen
- Notable: cityguard + knight guarding the entrance, ATM in the wall

### The Bar Of Swordsmen
- Exits: w -> Entrance Hall, s -> The Tournament And Practice Yard
- Notable: waiter NPC, bulletin board

### The Tournament And Practice Yard
- Exits: n -> The Bar Of Swordsmen, d -> a well leading into darkness
  (unexplored)
- Notable: guildmaster here — where warriors `practice` skills

### Main Street (West Gate jct)
- Exits: n -> unexplored (magic shop), e -> Main Street (Armory jct), s ->
  Guild of Magic Users (unexplored interior), w -> Inside The West Gate
- Notable: cityguard present

### Inside The West Gate Of Midgaard
- Exits: e -> Main Street (West Gate jct), s -> Wall Road (north end), w
  -> unexplored (outside the gate)
- Notable: cityguard guarding the gate

### Wall Road (north end)
- Exits: n -> Inside The West Gate, s -> Wall Road (mid)

### Wall Road (mid, "letters on wall")
- Exits: n -> Wall Road (north end), e -> Poor Alley (west end), s -> Wall
  Road (south end, bridge)
- Notable: writing on the wall not yet read

### Wall Road (south end, bridge)
- Exits: n -> Wall Road (mid), s -> a bridge across the river (unexplored)

## North of Midgaard / the newbie zone
This is where the minotaur goal (see player.md) is supposed to be. Route
in from Market Square: n, n, n, n (through Temple Square, The Temple Of
Midgaard, By The Temple Altar, Behind The Temple Altar) to The Great
Field Of Midgaard, then n again to the field's junction room, e into The
Entrance To The Newbie Zone, n into the maze.

### Behind The Temple Altar
- Exits: n -> The Great Field Of Midgaard, s -> By The Temple Altar
- Notable: mentions the Dragonhelm Mountains far north — unexplored,
  possibly relevant if the minotaur isn't in the maze itself

### The Great Field Of Midgaard (first room, from the temple)
- Exits: n -> The Great Field Of Midgaard (second room), s -> Behind The
  Temple Altar

### The Great Field Of Midgaard (second room, the junction)
- Exits: n -> unexplored, e -> The Entrance To The Newbie Zone, s -> The
  Great Field Of Midgaard (first room), w -> An Open Field By The Great
  Field (this is the maze's other exit, see below — the loop)

### The Entrance To The Newbie Zone
- Exits: n -> The Beginning Of The Passage, w -> The Great Field Of
  Midgaard (second room)

### The Beginning Of The Passage
- Exits: e -> The Dirty Hallway, s -> The Entrance To The Newbie Zone

### The Dirty Hallway
- Exits: e -> A Nexus, w -> The Beginning Of The Passage, s -> A Small
  Room (door was closed; open with `open door` then `south`)
- Notable: creepy crawler here — see Known Mobs, it's a real fight

### A Small Room
- Exits: n -> The Dirty Hallway, e -> More Of The Hallway (open with
  `open door e` — plain `open door`/`open east` didn't work here), (d) ->
  a well with a **locked** grate, needs a key we don't have
- Notable: Newbie Guard and a creepy crawler both present — see Known
  Mobs; verify target name before attacking, easy to mis-target

### A Nexus
- Exits: n -> unexplored, PITCH BLACK (needs a light source we don't
  have), (e) -> closed door, unexplored, s -> More Of The Hallway, w ->
  The Dirty Hallway
- Notable: room text claims north/east "brighten" but north was actually
  pitch black — don't trust the flavor text over what's actually shown

### More Of The Hallway
- Exits: n -> A Nexus, s -> Another Corner, w -> A Small Room
- Notable: creepy crawler here — see Known Mobs

### Another Corner
- Exits: n -> A Brighter Hallway, w -> unexplored, (e) -> closed door,
  unexplored
- Notable: newbie monster(s) here — see Known Mobs

### A Brighter Hallway
- Exits: e -> Another Corner, w -> The End Of The Passage
- Notable: newbie monster seen here too; "Someone's little pet dragon"
  seen loose here once (unconsidered, not seen consistently)

### The End Of The Passage
- Exits: e -> A Brighter Hallway, w -> An Open Field By The Great Field

### An Open Field By The Great Field
- Exits: e -> The End Of The Passage, n -> The Great Field Of Midgaard
  (second room)
- Notable: **this closes the loop** — the maze's lit west route dumps
  back out at the same field junction you enter from, just via its other
  exit. So the whole lit portion of the maze is a loop with no new ground
  outside it: the minotaur must be behind one of the remaining closed
  doors ((e) at Another Corner, (w)/A Small Room's side at More Of The
  Hallway, (s) at Dirty Hallway/A Small Room) or through the pitch-black
  room off A Nexus. Forcing those is the next real lead.

## Guild / practice locations
The single most useful thing to have pre-mapped, since finding a guild by
blind exploration burns a lot of turns.

- Warriors/fighters: **Guild of Swordsmen** — from The Bakery: s, e, e, e,
  s, e, s (Main St -> Market Sq -> Main St/Pet Shop jct -> Main St/weapon
  shop jct -> Entrance Hall -> Bar -> Practice Yard, guildmaster there)
- Clerics: Temple Square, west side (interior unexplored)
- Mages: Main Street West Gate jct, south side (interior unexplored)
- Thieves: Dark Alley, south side (interior unexplored)

## Known mobs
The only place mob combat data lives — see the note at the top of this
file before adding fight details anywhere else.

- **Massive minotaur** (the goal target): NOT YET FOUND, anywhere. Likely
  behind one of the maze's remaining closed doors or the pitch-black room
  — see "North of Midgaard" above. User tip (2026-07-18): there's
  supposedly a **"red room"** somewhere in the newbie zone where it might
  be — not yet located, keep an eye out for a room with unusual/red
  coloring or flavor text while exploring the still-closed doors. Given
  how much trouble even fidos and the Newbie Guard have caused at level 1
  bare-handed, do not approach this fight until noticeably stronger
  (leveled up, armed) — see player.md Goals/Hazards.
- **Fido** (beastly fido): Common Square, Guild of Swordsmen jct, West
  Gate jct. `consider` -> "The perfect match!" (even fight for level 1).
  Killable bare-handed but took 4 attempts before one didn't flee first;
  a kill drops ~10 gold + a piece of meat (edible). **Guard risk: killing
  one in a guarded room (Common Square, Market Square, Pet Shop jct,
  Guild of Swordsmen entrance, West Gate) draws the guard into attacking
  you too, and the guard is much more dangerous than the fido — got the
  character killed once.** See player.md Hazards. Fight only in
  guard-free rooms if actually trying to land a kill.
- **Newbie monster**: Another Corner, Dirty Hallway, and A Brighter
  Hallway, in the newbie zone maze (no guards anywhere in the maze).
  `consider` -> "You would need some luck!" (harder than fido). **0-for-2
  track record, regardless of starting HP or gear**: bare-handed at full
  HP it took us to 30% with no kill; with the dagger equipped starting at
  90% HP it dragged us all the way down to the `wimpy` auto-flee at 45%,
  again no kill. Room flavor text ("Kill him! Kill him!") badly undersells
  the actual difficulty. **Don't default to fighting this just because
  it's the nearest available mob — deprioritize it below fido and
  actively look elsewhere first**, since the fido has a real, proven
  track record with the dagger and this doesn't.
- **Newbie Guard**: A Small Room, in the maze. `consider` -> "The perfect
  match!" (same tier as fido). **Killed the character once** when the
  fight was left unmonitored — see player.md Hazards, this mob is not
  automatically safe just because it's guard-free territory.
- **Creepy little crawling thing**: wanders multiple maze rooms (Dirty
  Hallway, More Of The Hallway, A Small Room). Room flavor makes it read
  as harmless ambiance — **it is not**. Fought one (by accidental
  mis-target) and it took us from 100% to 35% HP for only ~1 exp, worse
  risk/reward than any other mob found so far.
- Green gelatinous blob: Poor Alley (west end), sucking in debris —
  unconsidered, treat with caution.
- odif yltsaeb ("fido" scrambled): Dark Alley, walking backwards — likely
  a joke/reversed mob, unconsidered.

## Points of interest

- **Fountain at Temple Square**: `drink fountain` gives free water, no
  gold needed — see player.md Hazards for why this matters (thirst stalls
  HP regen).
- ATM ("automatic teller machine"): Temple Of Midgaard, and Entrance Hall
  To The Guild Of Swordsmen.
- The Grunting Boar Inn: east of Temple Square (interior unexplored).
- The Grubby Inn: south of The Eastern End Of Poor Alley (interior
  unexplored).
- Bakery prices: danish pastry 7g, bread 15g, waybread 75g.
