#!/usr/bin/env python3
import os, socket, time, threading, sys
IN_FIFO='/tmp/mud_in_fifo'
OUT_LOG='/tmp/mud_out.log'
HOST='localhost'; PORT=4000
NAME='dummy'; PW='helloworld'

# create fifo if needed
if not os.path.exists(IN_FIFO):
    try:
        os.mkfifo(IN_FIFO)
    except Exception as e:
        print('Failed to create fifo', e); sys.exit(1)

# helper to append to out log
def append_out(s):
    with open(OUT_LOG,'a',encoding='utf-8',errors='ignore') as f:
        f.write(s)

# connect to MUD
s = socket.create_connection((HOST,PORT),timeout=10)
s.settimeout(0.5)

def recv_all(timeout=0.2):
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

append_out('\n--- PROXY STARTED ---\n')
append_out(recv_all(0.8))
# send name
s.sendall((NAME+'\n').encode())
append_out('\n--- SENT NAME ---\n')
append_out(recv_all(0.8))
# try auto-confirm
if os.path.exists('/tmp/mud_auto_confirm'):
    s.sendall(b'y\n')
    append_out('\n--- SENT AUTO-CONFIRM Y ---\n')
    append_out(recv_all(0.8))
else:
    # always try to send 'y' if server asks
    out = recv_all(0.2)
    if 'did i get that' in out.lower() or 'are you sure' in out.lower() or 'y/n' in out.lower():
        s.sendall(b'y\n')
        append_out('\n--- SENT CONFIRM Y ---\n')
        append_out(recv_all(0.8))
# send password if requested
out = recv_all(0.2)
if 'password' in out.lower():
    s.sendall((PW+'\n').encode())
    append_out('\n--- SENT PASSWORD ---\n')
    append_out(recv_all(0.8))

append_out('\n--- READY FOR COMMANDS ---\n')

# background thread to read fifo and send to MUD

def fifo_reader():
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
                            s.close()
                        except:
                            pass
                        os._exit(0)
                    try:
                        s.sendall((cmd+'\n').encode())
                    except Exception as e:
                        append_out('\n--- SEND FAILED: '+repr(e)+' ---\n')
                        # try reconnect
                        try:
                            s2 = socket.create_connection((HOST,PORT),timeout=10)
                            s2.settimeout(0.5)
                            s.send = s2.send
                            append_out('\n--- RECONNECTED ---\n')
                        except Exception as e2:
                            append_out('\n--- RECONNECT FAILED: '+repr(e2)+' ---\n')
                    # gather response
                    time.sleep(0.25)
                    resp = recv_all(0.8)
                    if resp:
                        append_out('\n--- RESP FOR: '+cmd+' ---\n')
                        append_out(resp)
        except Exception as e:
            append_out('\n--- FIFO READ ERROR: '+repr(e)+' ---\n')
            time.sleep(0.5)

thr = threading.Thread(target=fifo_reader, daemon=True)
thr.start()

# keep main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    append_out('\n--- PROXY STOPPED BY SIGINT ---\n')
    try:
        s.close()
    except:
        pass

