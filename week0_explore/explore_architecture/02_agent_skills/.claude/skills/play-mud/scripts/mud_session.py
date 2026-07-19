#!/usr/bin/env python3
"""
Persistent telnet session manager for tbaMUD/CircleMUD-based MUD servers.

A MUD connection is stateful (login, room position, combat, buffs...) but each
Bash tool call from Claude is a fresh process. This script solves that by
running a small background daemon that holds the actual telnet socket open,
and a lightweight CLI that talks to the daemon over a Unix domain socket to
send commands and fetch the resulting output.

Subcommands:
  start   [--host HOST] [--port PORT] [--state-dir DIR]
          Launch the background daemon and connect to the MUD.

  login   [--name NAME] [--password PASS] [--state-dir DIR]
          Drive the standard CircleMUD/tbaMUD login handshake
          (name -> password -> MOTD "press return" paging) using
          quiet-period detection rather than exact prompt matching,
          since prompt text varies between MUD codebases/configs.

  send TEXT [--wait SECONDS] [--state-dir DIR]
          Send one line of input (a command) and return whatever the
          MUD prints in response, waiting for output to go quiet.

  read    [--state-dir DIR]
          Return recent buffered output WITHOUT sending anything.
          Use this to check for async events (you were attacked, a
          tell came in, etc.) between commands.

  status  [--state-dir DIR]
          Report whether the daemon is running and connected.

  stop    [--state-dir DIR]
          Send "quit", close the connection, and terminate the daemon.

State (pid, control socket, transcript log) lives in --state-dir, which
defaults to /tmp/mud-session-<port>/ so it's stable across separate tool
calls without the caller having to track anything.
"""
import argparse
import json
import os
import selectors
import signal
import socket
import sys
import threading
import time

IAC, DONT, DO, WONT, WILL, SB, SE = 255, 254, 253, 252, 251, 250, 240


class TelnetFilter:
    """Strips/answers telnet IAC negotiation, yielding clean text.

    Buffers a trailing partial IAC sequence across feed() calls so option
    negotiation bytes never leak into the transcript even if they land on
    a read() boundary.
    """

    def __init__(self, sock):
        self.sock = sock
        self._pending = b""

    def feed(self, data: bytes) -> str:
        data = self._pending + data
        self._pending = b""
        out = bytearray()
        i, n = 0, len(data)
        while i < n:
            b = data[i]
            if b != IAC:
                out.append(b)
                i += 1
                continue
            if i + 1 >= n:
                self._pending = data[i:]
                break
            cmd = data[i + 1]
            if cmd in (WILL, WONT, DO, DONT):
                if i + 2 >= n:
                    self._pending = data[i:]
                    break
                opt = data[i + 2]
                try:
                    if cmd == WILL:
                        self.sock.sendall(bytes([IAC, DONT, opt]))
                    elif cmd == DO:
                        self.sock.sendall(bytes([IAC, WONT, opt]))
                except OSError:
                    pass
                i += 3
            elif cmd == SB:
                j = i + 2
                while j + 1 < n and not (data[j] == IAC and data[j + 1] == SE):
                    j += 1
                if j + 1 >= n:
                    self._pending = data[i:]
                    break
                i = j + 2
            elif cmd == IAC:
                out.append(IAC)
                i += 2
            else:
                i += 2
        return out.decode("latin-1")


class MudDaemon:
    QUIET_GAP = 0.4       # seconds of silence that counts as "done responding"
    DEFAULT_MAX_WAIT = 3.0  # hard cap per send, in case the MUD stays chatty

    def __init__(self, host, port, state_dir):
        self.host, self.port, self.state_dir = host, port, state_dir
        self.buf = []            # list of str chunks, append-only
        self.buf_lock = threading.Lock()
        self.last_recv = time.monotonic()
        self.sock = None
        self.filt = None
        self.running = True

    def connect(self):
        self.sock = socket.create_connection((self.host, self.port), timeout=10)
        self.sock.settimeout(0.5)
        self.filt = TelnetFilter(self.sock)

    def _log_path(self):
        return os.path.join(self.state_dir, "session.log")

    def reader_loop(self):
        log = open(self._log_path(), "a", buffering=1)
        while self.running:
            try:
                data = self.sock.recv(4096)
            except socket.timeout:
                continue
            except OSError:
                break
            if not data:
                break
            text = self.filt.feed(data)
            if text:
                with self.buf_lock:
                    self.buf.append(text)
                    self.last_recv = time.monotonic()
                log.write(text)
        log.close()

    def buffer_len(self):
        with self.buf_lock:
            return len("".join(self.buf))

    def buffer_text(self):
        with self.buf_lock:
            return "".join(self.buf)

    def capture_after(self, text, max_wait):
        """Optionally send `text`, then read until output goes quiet."""
        start_len = self.buffer_len()
        if text is not None:
            try:
                self.sock.sendall((text + "\r\n").encode("latin-1", "replace"))
            except OSError:
                return "", False
        deadline = time.monotonic() + max_wait
        while True:
            time.sleep(0.1)
            with self.buf_lock:
                quiet_for = time.monotonic() - self.last_recv
            if quiet_for >= self.QUIET_GAP:
                break
            if time.monotonic() >= deadline:
                break
        full = self.buffer_text()
        return full[start_len:], True

    def handle_request(self, req):
        cmd = req.get("cmd")
        if cmd == "send":
            out, ok = self.capture_after(req.get("text"), req.get("max_wait", self.DEFAULT_MAX_WAIT))
            return {"ok": ok, "output": out}
        if cmd == "read":
            n = req.get("chars", 4000)
            return {"ok": True, "output": self.buffer_text()[-n:]}
        if cmd == "status":
            return {"ok": True, "connected": self.sock is not None, "buffer_chars": self.buffer_len()}
        if cmd == "stop":
            self.capture_after("quit", 1.5)
            self.running = False
            try:
                self.sock.close()
            except OSError:
                pass
            return {"ok": True}
        return {"ok": False, "error": f"unknown cmd {cmd!r}"}

    def control_loop(self, ctrl_sock_path):
        srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if os.path.exists(ctrl_sock_path):
            os.remove(ctrl_sock_path)
        srv.bind(ctrl_sock_path)
        srv.listen(8)
        srv.settimeout(0.5)
        sel = selectors.DefaultSelector()
        while self.running:
            try:
                conn, _ = srv.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            try:
                conn.settimeout(10)
                data = b""
                while b"\n" not in data:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                if data:
                    req = json.loads(data.decode("utf-8").strip())
                    resp = self.handle_request(req)
                    conn.sendall((json.dumps(resp) + "\n").encode("utf-8"))
            except Exception as e:
                try:
                    conn.sendall((json.dumps({"ok": False, "error": str(e)}) + "\n").encode("utf-8"))
                except OSError:
                    pass
            finally:
                conn.close()
        srv.close()
        if os.path.exists(ctrl_sock_path):
            os.remove(ctrl_sock_path)


def daemon_main(args):
    os.makedirs(args.state_dir, exist_ok=True)
    d = MudDaemon(args.host, args.port, args.state_dir)
    d.connect()
    with open(os.path.join(args.state_dir, "daemon.pid"), "w") as f:
        f.write(str(os.getpid()))
    reader = threading.Thread(target=d.reader_loop, daemon=True)
    reader.start()

    def handle_term(signum, frame):
        d.running = False

    signal.signal(signal.SIGTERM, handle_term)
    signal.signal(signal.SIGINT, handle_term)
    d.control_loop(os.path.join(args.state_dir, "control.sock"))


def rpc(state_dir, req, timeout=10):
    path = os.path.join(state_dir, "control.sock")
    if not os.path.exists(path):
        return {"ok": False, "error": "no session running (control socket missing) -- run 'start' first"}
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect(path)
        s.sendall((json.dumps(req) + "\n").encode("utf-8"))
        data = b""
        while b"\n" not in data:
            chunk = s.recv(65536)
            if not chunk:
                break
            data += chunk
        return json.loads(data.decode("utf-8").strip())
    except OSError as e:
        return {"ok": False, "error": f"could not reach daemon: {e}"}
    finally:
        s.close()


def cmd_start(args):
    os.makedirs(args.state_dir, exist_ok=True)
    pid_file = os.path.join(args.state_dir, "daemon.pid")
    if os.path.exists(pid_file):
        try:
            pid = int(open(pid_file).read().strip())
            os.kill(pid, 0)
            print(f"Session already running (pid {pid}) in {args.state_dir}")
            return
        except (OSError, ValueError):
            pass  # stale pidfile, fall through and start fresh

    daemon_log = open(os.path.join(args.state_dir, "daemon.stderr.log"), "a")
    subprocess_args = [
        sys.executable, os.path.abspath(__file__), "_daemon",
        "--host", args.host, "--port", str(args.port),
        "--state-dir", args.state_dir,
    ]
    import subprocess
    subprocess.Popen(
        subprocess_args,
        stdout=daemon_log, stderr=daemon_log,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )
    ctrl_path = os.path.join(args.state_dir, "control.sock")
    for _ in range(50):
        if os.path.exists(ctrl_path):
            break
        time.sleep(0.1)
    else:
        print("Daemon did not come up in time; check daemon.stderr.log", file=sys.stderr)
        sys.exit(1)
    resp = rpc(args.state_dir, {"cmd": "read", "chars": 4000})
    print(f"Connected to {args.host}:{args.port}. Initial output:\n")
    print(resp.get("output", ""))


def cmd_login(args):
    """Heuristic CircleMUD/tbaMUD login: name -> password -> page through MOTD.

    Uses quiet-period waits instead of matching exact prompt strings, since
    those vary by mud config. If this doesn't complete cleanly, use `read`
    to see the raw transcript and finish the handshake manually with `send`.
    """
    transcript = []

    def step(text, max_wait=2.5):
        resp = rpc(args.state_dir, {"cmd": "send", "text": text, "max_wait": max_wait})
        out = resp.get("output", "")
        transcript.append(out)
        return out

    out = step(args.name)
    lower = out.lower()
    if "yes or no" in lower or "(y/n)" in lower:
        # Name-spelling confirmation -- normally only shown for a name the
        # server has never seen before. Answering "yes" here creates a new
        # character, so don't do that automatically on behalf of the user.
        print("".join(transcript))
        print(
            f"\n[login] Server is asking to confirm the spelling of {args.name!r}, "
            "which usually means this name doesn't exist yet. Stopping here instead "
            "of auto-confirming, since that would create a new character. If that's "
            "actually what you want, answer by hand with `send yes` and continue the "
            "creation prompts manually.",
            file=sys.stderr,
        )
        sys.exit(2)
    if "password" not in lower and "new" not in lower:
        # Give the server a bit longer in case the banner was still printing.
        out += step(None, max_wait=1.5)

    if "new" in out.lower() and "password" not in out.lower():
        print("".join(transcript))
        print(
            "\n[login] Server output suggests this may be a NEW character "
            f"creation flow rather than an existing login for {args.name!r}. "
            "Stopping here -- inspect the transcript above and drive the "
            "rest of character creation manually with `send`, or confirm "
            "the account already exists before retrying.",
            file=sys.stderr,
        )
        sys.exit(2)

    if args.password:
        step(args.password)

    # Page through MOTD / "press return to continue" screens, and answer the
    # post-login account menu ("0) Exit  1) Enter the game  2) ...") that
    # tbaMUD presents by choosing "1". Keep going only while the response
    # still looks like a continuation/menu prompt; stop as soon as it
    # doesn't, so we don't feed spurious input once we've landed in the world.
    continue_cues = ("return", "continue", "more", "press", "enter")
    for _ in range(6):
        if "make your choice" in out.lower() or "enter the game" in out.lower():
            out = step("1", max_wait=2.0)
            continue
        out = step("", max_wait=1.2)
        if not out.strip():
            break
        if not any(cue in out.lower() for cue in continue_cues) and "make your choice" not in out.lower():
            break

    print("".join(transcript))


def cmd_send(args):
    resp = rpc(args.state_dir, {"cmd": "send", "text": args.text, "max_wait": args.wait})
    if not resp.get("ok", True) and "error" in resp:
        print(f"error: {resp['error']}", file=sys.stderr)
        sys.exit(1)
    print(resp.get("output", ""))


def cmd_read(args):
    resp = rpc(args.state_dir, {"cmd": "read", "chars": args.chars})
    print(resp.get("output", ""))


def cmd_status(args):
    resp = rpc(args.state_dir, {"cmd": "status"})
    print(json.dumps(resp, indent=2))


def cmd_stop(args):
    resp = rpc(args.state_dir, {"cmd": "stop"})
    pid_file = os.path.join(args.state_dir, "daemon.pid")
    if os.path.exists(pid_file):
        try:
            os.remove(pid_file)
        except OSError:
            pass
    print(json.dumps(resp, indent=2))


def default_state_dir(port):
    return os.environ.get("MUD_STATE_DIR") or f"/tmp/mud-session-{port}"


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="subcommand", required=True)

    def add_state_dir(sp, port_default=4000):
        sp.add_argument("--state-dir", default=None)

    sp = sub.add_parser("start", help="connect to the MUD and start the background session")
    sp.add_argument("--host", default="localhost")
    sp.add_argument("--port", type=int, default=4000)
    add_state_dir(sp)
    sp.set_defaults(func=cmd_start)

    sp = sub.add_parser("_daemon", help=argparse.SUPPRESS)  # internal, spawned by `start`
    sp.add_argument("--host", required=True)
    sp.add_argument("--port", type=int, required=True)
    sp.add_argument("--state-dir", required=True)
    sp.set_defaults(func=daemon_main)

    sp = sub.add_parser("login", help="run the standard name/password/MOTD login handshake")
    sp.add_argument("--name", default="dummy")
    sp.add_argument("--password", default=os.environ.get("MUD_PASSWORD"))
    sp.add_argument("--port", type=int, default=4000)
    add_state_dir(sp)
    sp.set_defaults(func=cmd_login)

    sp = sub.add_parser("send", help="send one command and return the MUD's response")
    sp.add_argument("text", help="command text, e.g. 'look', 'north', \"say hello\"")
    sp.add_argument("--wait", type=float, default=MudDaemon.DEFAULT_MAX_WAIT)
    sp.add_argument("--port", type=int, default=4000)
    add_state_dir(sp)
    sp.set_defaults(func=cmd_send)

    sp = sub.add_parser("read", help="show recent output without sending anything")
    sp.add_argument("--chars", type=int, default=4000)
    sp.add_argument("--port", type=int, default=4000)
    add_state_dir(sp)
    sp.set_defaults(func=cmd_read)

    sp = sub.add_parser("status", help="check whether the session is up")
    sp.add_argument("--port", type=int, default=4000)
    add_state_dir(sp)
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("stop", help="quit and tear down the session")
    sp.add_argument("--port", type=int, default=4000)
    add_state_dir(sp)
    sp.set_defaults(func=cmd_stop)

    return p


def main():
    args = build_parser().parse_args()
    if args.state_dir is None:
        args.state_dir = default_state_dir(args.port)
    args.func(args)


if __name__ == "__main__":
    main()
