# Common tbaMUD / CircleMUD commands

CircleMUD-derived codebases (tbaMUD is one of them) share a large common
command vocabulary. Exact availability can vary by mud config/area, so treat
this as a strong prior, not a guarantee — if a command returns "Huh?!?" try
an obvious synonym.

## Movement
- `north` / `n`, `south` / `s`, `east` / `e`, `west` / `w`
- `up` / `u`, `down` / `d`
- `northeast` / `ne`, `northwest` / `nw`, `southeast` / `se`, `southwest` / `sw`
- `enter <portal/door>`, `exit`

## Observation
- `look` / `l` — describe the current room
- `look <direction>` — peek without moving
- `look <object/mob>` / `examine <object>` — inspect something
- `exits` — list obvious exits
- `who` — list players online
- `where` — list nearby players (imm-only on some muds)
- `score` / `sc` — character stats (hp, mv, level, alignment...)
- `inventory` / `i` — items you're carrying
- `equipment` / `eq` — items you're wearing/wielding

## Communication
- `say <text>` or `'<text>` — talk to the room
- `tell <name> <text>` — private message
- `gossip <text>`, `shout <text>`, `auction <text>` — global channels (name varies by mud)
- `emote <action>` — custom emote, shows as "YourName <action>"
- `reply <text>` — reply to the last tell you received

## Items
- `get <item>` / `get <item> <container>` — pick up
- `drop <item>`
- `wear <item>`, `wield <item>`, `hold <item>`, `remove <item>`
- `give <item> <person>`
- `put <item> <container>`
- `open <object>` / `close <object>` (doors, containers)

## Combat
- `kill <target>` / `k <target>` — initiate combat
- `flee` — attempt to escape combat
- `consider <target>` / `con <target>` — gauge difficulty before engaging
- `cast '<spell name>' <target>` — cast a spell (quotes matter on most CircleMUD forks)
- `hit <target>` — melee attack (some codebases alias this to kill)

## Character / meta
- `save` — force a save of your character
- `quit` — leave the game (the skill's `stop` subcommand does this for you)
- `help <topic>` — in-game help; useful for discovering area-specific commands
- `practice` / `prac` — check/improve skills and spells (class-dependent)

## Tips for driving this via the skill
- After any command that might trigger asynchronous output (combat, other
  players' actions), use `read` (not `send`) to check for new events without
  taking another action.
- If a command returns `Huh?!?`, that verb isn't recognized here — try `help`
  or a listed synonym above rather than guessing repeatedly.
- Prompts commonly look like `<850hp 100mv>` or similar; that's not part of
  room description text, it's the mud's status line.
