#!/usr/bin/env python3
import os, socket, time, threading, sys
IN_FIFO='/tmp/mud_in_fifo'
OUT_LOG='/tmp/mud_out.log'
HOST='localhost'; PORT=4000
NAME='dummy'; PW='helloworld'

# ensure log exists
open(OUT_LOG,'a').close()

# create fifo if needed
if not os.path.exists(IN_FIFO):
    try:
        os.mkfifo(IN_FIFO)
    except Exception as e:
        print('Failed to create fifo', e); sys.exit(1)

sock_lock = threading.Lock()
sock = None

def append_out(s):
    try:
        with open(OUT_LOG,'a',encoding='utf-8',errors='ignore') as f:
            f.write(s)
    except Exception:
        pass

def recv_all(s, timeout=0.2):
    s.settimeout(timeout)
    out=''
    try:
        while True:
            data = s.recv(8192)
            if not data:
                break
            out += data.decode('utf-8',errors='ignore')
    except Exception:
        pass
    return out

def connect_and_login():
    global sock
    while True:
        try:
            s = socket.create_connection((HOST,PORT),timeout=8)
            s.settimeout(0.5)
            with sock_lock:
                sock = s
            append_out('\n--- PROXY STARTED (v2) ---\n')
            append_out(recv_all(s,0.8))
            # send name
            s.sendall((NAME+'\n').encode())
            append_out('\n--- SENT NAME ---\n')
            append_out(recv_all(s,0.6))
            # try confirm 'y'
            try:
                s.sendall(b'y\n')
                append_out('\n--- SENT AUTO-CONFIRM Y ---\n')
                append_out(recv_all(s,0.6))
            except Exception:
                pass
            # send password
            try:
                s.sendall((PW+'\n').encode())
                append_out('\n--- SENT PASSWORD ---\n')
                append_out(recv_all(s,0.6))
            except Exception:
                pass
            append_out('\n--- READY FOR COMMANDS ---\n')
            return
        except Exception as e:
            append_out('\n--- CONNECT/LOGIN FAILED: '+repr(e)+' ---\n')
            time.sleep(1)

# reader thread: read lines from fifo and send to MUD

def fifo_reader():
    global sock
    while True:
        try:
            with open(IN_FIFO, 'r', encoding='utf-8', errors='ignore') as fifo:
                for line in fifo:
                    cmd = line.rstrip('\n')
                    if not cmd:
                        continue
                    if cmd.lower() == 'exitproxy':
                        append_out('\n--- PROXY EXITING ---\n')
                        try:
                            with sock_lock:
                                if sock:
                                    sock.close()
                        except:
                            pass
                        os._exit(0)
                    sent=False
                    for attempt in range(3):
                        try:
                            with sock_lock:
                                if not sock:
                                    break
                                sock.sendall((cmd+'\n').encode())
                                sent=True
                                break
                        except Exception as e:
                            append_out('\n--- SEND FAILED: '+repr(e)+' ---\n')
                            # try reconnect
                            try:
                                with sock_lock:
                                    if sock:
                                        try: sock.close()
                                        except: pass
                                    sock = None
                            except:
                                pass
                            connect_and_login()
                    if not sent:
                        append_out('\n--- GIVING UP SENDING: '+cmd+' ---\n')
                        continue
                    # gather response
                    time.sleep(0.3)
                    try:
                        with sock_lock:
                            resp = recv_all(sock,0.6) if sock else ''
                    except Exception as e:
                        resp = '\n--- RECV ERROR: '+repr(e)+' ---\n'
                    if resp:
                        append_out('\n--- RESP FOR: '+cmd+' ---\n')
                        append_out(resp)
        except Exception as e:
            append_out('\n--- FIFO READ ERROR: '+repr(e)+' ---\n')
            time.sleep(0.8)

if __name__ == '__main__':
    connect_and_login()
    thr = threading.Thread(target=fifo_reader, daemon=True)
    thr.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        append_out('\n--- PROXY STOPPED BY SIGINT ---\n')
        try:
            with sock_lock:
                if sock: sock.close()
        except:
            pass

