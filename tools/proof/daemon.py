#!/usr/bin/env python3
"""Persistent bench for the proof playthrough: starts ScummVM once (tools/bench.py's
Bench, developer mode off) and serves step lists on 127.0.0.1:47123, one JSON list
per connection; answers with the bench's printed lines."""
import io, json, os, socket, subprocess, sys, contextlib, time
R = '/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky'
sys.path.insert(0, os.path.join(R, 'tools'))
import bench  # noqa

G = "/Users/simonstark/Library/Developer/CoreSimulator/Devices/28091D11-A25F-4C5D-B4C3-E0773C1C3E78/data/Containers/Data/Application/2AB2B466-7AB0-4BE8-85A0-98264DF04E6E/Documents/Grim Fandango/Game"
S = os.path.dirname(os.path.abspath(__file__))
LABS = os.path.join(R, 'build', 'proof-bench', 'labs')
os.environ.setdefault("X","1")
b = bench.Bench(G, os.path.expanduser('~/Developer/pointyclicky-build/grim-bench/scummvm'), LABS)
print('bench up', b.proc.pid, flush=True)
srv = socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(('127.0.0.1', 47123))
srv.listen(1)
try:
    while True:
        c, _ = srv.accept()
        data = b''
        while not data.endswith(b'\n'):
            chunk = c.recv(65536)
            if not chunk:
                break
            data += chunk
        steps = json.loads(data)
        out = io.StringIO()
        try:
            if steps == 'quit':
                c.sendall(b'bye\n'); c.close(); break
            if b.proc.poll() is not None:
                out.write('SCUMMVM DIED rc=%s\n' % b.proc.returncode)
            else:
                with contextlib.redirect_stdout(out):
                    for st in steps:
                        if 'hold' in st:  # press, wait, release at one point
                            x, y = st['hold']
                            print('button', b.call('button', x=x, y=y, down=1))
                            time.sleep(st.get('for', 1.0))
                            print('button', b.call('button', x=x, y=y, down=0))
                        elif 'dbl' in st:  # double tap = run
                            x, y = st['dbl']
                            print('click', b.call('click', x=x, y=y, button=1))
                            time.sleep(0.12)
                            print('click', b.call('click', x=x, y=y, button=1))
                        elif 'look' in st:  # two-finger tap = right button
                            x, y = st['look']
                            print('click', b.call('click', x=x, y=y, button='right'))
                        elif 'stamp' in st:  # the wall clock, for timing a tap to the game's beat
                            print('stamp %.3f' % time.time())
                        elif 'at' in st:  # wait until a wall-clock time, then the step in 'then'
                            time.sleep(max(0, st['at'] - time.time()))
                            bench.run(b, [st['then']])
                            print('stamp %.3f' % time.time())
                        elif 'onbeat' in st:  # shoot until a region of the screen changes, then after 'delay' s the step in 'then'
                            g, thr, below = st['onbeat'], st['thr'], st.get('below', False)
                            tmp = os.path.join(R, 'build', 'proof-bench', 'beat.png')
                            def look():
                                b.call('shot', path=tmp)
                                v = float(subprocess.run(['magick', tmp, '-crop', g, '+repage', '-colorspace', 'gray', '-format',
                                                          '%[fx:mean*1000]', 'info:'], capture_output=True, text=True).stdout)
                                return v < thr if below else v > thr
                            prev, t0 = True, None
                            for _ in range(st.get('max', 60)):
                                h = look()
                                if h and not prev:
                                    t0 = time.time()
                                    break
                                prev = h
                            if t0 is None:
                                print('onbeat: none seen')
                            else:
                                while time.time() < t0 + st['delay']:
                                    look()
                                bench.run(b, [st['then']])
                                print('onbeat: seen %.3f, then at %.3f' % (t0, time.time()))
                        elif 'skip' in st:
                            print('skip', b.call('skip'))
                        else:
                            bench.run(b, [st])
        except Exception as e:  # noqa
            out.write('ERROR %r\n' % e)
        if b.proc.poll() is not None:
            out.write('SCUMMVM DIED rc=%s\n' % b.proc.returncode)
        c.sendall(out.getvalue().encode() + b'\n')
        c.close()
finally:
    b.stop()
