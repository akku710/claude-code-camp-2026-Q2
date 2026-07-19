---
name: play-mud
description: Play a tbaMUD/CircleMUD-based MUD (text-based multiplayer game) running on localhost, using the "dummy" character, and pursue long-running goals (like reaching a target level or hunting down a specific monster) across many separate play sessions. Use this whenever the user asks to connect to, log into, or play a MUD, talk about their character "dummy", or wants to explore rooms, fight monsters, chat, or manage inventory on a local telnet-based game server (typically localhost:4000). Also use it whenever the user asks to check on the MUD, see what's happening in-game, check progress toward a MUD goal, or issue any in-game command (look, move, kill, say, inventory, score, etc.) — don't wait for them to explicitly mention "telnet" or "skill".
---

# Playing a tbaMUD/CircleMUD MUD

This skill drives a live telnet session against a local MUD server (default
`localhost:4000`) as the character `dummy`. It's built around a small
background daemon because a MUD connection is stateful — login, room
position, combat, HP — but each Bash tool call you make is a fresh process.
The daemon holds the actual socket open between your calls.

That daemon's state only lasts for the current play session, though — it
lives under `/tmp` and dies with the process. Goals like "reach level 7" or
"defeat the swamp troll" take many separate sessions (and separate
conversations) to finish, so this skill also keeps durable notes in
`data/player.md` (character state and goals) and `data/world.md` (map and
world knowledge) that persist across all of that. Treat those two files as
the character's actual memory — the MUD itself has no idea you're pursuing
a goal, so if you don't write it down, it's gone the moment this
conversation ends.

All interaction goes through `scripts/mud_session.py`. Run it with `python3`.

## Workflow

0. **Read the memory files first**, before touching the MUD connection:
   `data/player.md` for goals, last-known status, and learned skills, and
   `data/world.md` for the map and anything already known about guilds and
   mobs. This is what lets you pick up where a previous session left off
   instead of re-exploring rooms or re-deriving the goal from scratch. If
   the user gave you something specific to do this session, do that; if
   they just said "play" or "keep going," let the open goals in
   `player.md` drive what you do next.

1. **Start the session** (once per play session):
   ```
   python3 scripts/mud_session.py start
   ```
   This connects to the MUD and prints whatever banner/prompt it sends. If
   the server isn't reachable you'll get a clear connection error — check
   the MUD process is actually running on port 4000 before debugging further.

2. **Log in**:
   ```
   python3 scripts/mud_session.py login --name dummy --password helloworld
   ```
   This drives the standard name → password → MOTD-paging → account-menu
   handshake. The password can also be set via the `MUD_PASSWORD` env var to
   avoid it appearing in shell history/process args.

   The login step uses quiet-period detection (waits for the MUD to stop
   sending data) rather than matching an exact prompt string, since prompt
   wording differs between mud configs. If the printed transcript doesn't
   look like a successful login (e.g. it looks like new-character creation,
   or gets stuck), don't retry blindly — use `read` to see the raw
   transcript, then finish the handshake by hand with individual `send`
   calls, mirroring whatever the transcript shows is being asked for.

3. **Play**, one action at a time:
   ```
   python3 scripts/mud_session.py send "look"
   python3 scripts/mud_session.py send "north"
   python3 scripts/mud_session.py send "kill rat"
   python3 scripts/mud_session.py send "say hello!"
   ```
   Each call returns the MUD's response to that command. See
   `data/circlemud_commands.md` for the standard command vocabulary
   (movement, combat, communication, items) — check it before guessing at
   command syntax.

4. **Check for async events** between actions (someone tells you something,
   a mob attacks you, HP changes from a DoT) without taking an action:
   ```
   python3 scripts/mud_session.py read
   ```
   This is important during or after combat — the MUD keeps sending
   messages on its own timer, not just in response to what you type.

5. **Update the memory files as you go**, not just at the end. Update
   `data/world.md` the moment you learn something reusable — a room's exits,
   where a guild or guildmaster is, where a mob spawns — the same way you'd
   jot down a map while exploring a place for the first time. Update
   `data/player.md` whenever status that matters for planning changes:
   level up, a skill's proficiency improves, a goal gets checked off, or
   `score` reveals something the file had wrong. Doing this incrementally
   means a dropped connection or an interrupted conversation doesn't erase
   progress. When editing, keep the file's existing structure (headings,
   checkboxes, format shown in the templates) rather than reformatting it —
   these files get read and re-edited across many sessions, so a stable
   shape matters more than making any one edit look tidy.

6. **Stop the session** when done (or before starting a fresh one):
   ```
   python3 scripts/mud_session.py stop
   ```
   This sends `quit` gracefully and tears down the daemon. If a session
   seems stuck, `status` will tell you if the daemon is even still up.

   Before stopping, make sure `data/player.md` and `data/world.md` reflect
   where things actually stand — update the "Last updated" line and add one
   line to the Session Log in `player.md` summarizing what happened and
   what to pick up next time. That log entry is often the single most
   useful thing for a future session, since it's a plain summary rather
   than something that has to be reconstructed from the rest of the file.

## Notes

- Session state (pid, control socket, transcript log) lives in
  `/tmp/mud-session-<port>/` by default, so it survives across your separate
  tool calls without you needing to track anything. Override with
  `--state-dir` if running multiple concurrent sessions (e.g. different
  characters or servers).
- If `--host`/`--port` differ from `localhost:4000`, pass them consistently
  to every subcommand (or export `MUD_STATE_DIR` so they all agree on the
  same session).
- Don't call `start` again if a session is already running — it detects and
  reuses the existing one. Use `status` if you're unsure whether one is up.
- The script strips raw telnet protocol bytes (IAC negotiation) itself, so
  what you see from `send`/`read` is clean game text — no need to filter it
  yourself.
- `data/player.md` and `data/world.md` ship with placeholder content the
  first time this skill is used — fill them in for real as you play rather
  than leaving the placeholders in place. If a goal placeholder like
  "<set target monster>" is still unfilled when it becomes relevant, ask
  the user rather than guessing.
