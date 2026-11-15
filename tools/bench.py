#!/usr/bin/env python3
"""The test bench: Grim Fandango on the Mac in a ScummVM built with this
edition and PointyClicky's control server (walkthroughs/rig), driven from
here: keys, pointer moves and clicks, screenshots.

    python3 -I tools/bench.py <grim folder> <scummvm binary> <lab dir> <script.json>

<grim folder> is your own copy; <lab dir> holds grim-pointyclicky.lab (as
grim-mouse.lab) and ScummVM's grim-patch.lab. The script is a list of steps:
  {"wait": 2.5}                      seconds
  {"key": "i"} / {"key": "esc"} / {"key": "left"}
  {"move": [x, y]} / {"click": [x, y], "button": 1}
  {"shot": "name"}                   -> build/bench/name.png
  {"save": 1} / {"load": 1}          the engine's own save / load, slot n
Everything is written under build/bench (git-ignored). BENCH_DEBUG=1 draws
every outline (grim_mouse_debug).
"""
import json
import os
import socket
import subprocess
import sys
import time

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
KEYS = {'esc': (27, 27), 'left': (276, 0), 'right': (275, 0), 'up': (273, 0), 'down': (274, 0),
        'enter': (13, 13), 'space': (32, 32)}

INI = """[scummvm]
gfx_mode=surfacesdl
scale_factor=1
scaler=normal
mute=true
music_driver=null
confirm_exit=false
gui_return_to_launcher_at_exit=false
grim_mouse=true
renderer=software
subtitles=true
"""


class Bench:
    def __init__(self, game, binary, labs):
        self.out = os.path.join(ROOT, 'build', 'bench')
        os.makedirs(os.path.join(self.out, 'saves'), exist_ok=True)
        ini = os.path.join(self.out, 'scummvm.ini')
        # BENCH_DEBUG=1: every outline drawn (grim_mouse_debug)
        open(ini, 'w').write(INI + ('grim_mouse_debug=true\n' if os.environ.get('BENCH_DEBUG') else ''))
        self.sock_path = '/tmp/grim-bench.sock'
        try:
            os.unlink(self.sock_path)
        except FileNotFoundError:
            pass
        env = dict(os.environ, PT_RIG_SOCKET=self.sock_path, PT_RIG_SPEED='1',
                   SDL_VIDEODRIVER='dummy', SDL_RENDER_DRIVER='software', SDL_AUDIODRIVER='dummy')
        self.log = open(os.path.join(self.out, 'scummvm.out'), 'w')
        self.proc = subprocess.Popen([binary, f'--config={ini}', f'--path={game}', '--savepath=' + os.path.join(self.out, 'saves'),
                                      f'--extrapath={labs}', '--renderer=software', '-d1', 'grim'],
                                     env=env, stdout=self.log, stderr=subprocess.STDOUT)
        self.sock, self.buf, self.n = None, b'', 0
        for _ in range(300):
            try:
                s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                s.connect(self.sock_path)
                self.sock = s
                break
            except OSError:
                time.sleep(0.1)
        if not self.sock:
            self.stop()
            sys.exit('bench: no connection to the rig')

    def call(self, op, **args):
        self.n += 1
        self.sock.sendall((json.dumps(dict(op=op, id=self.n, **args)) + '\n').encode())
        while b'\n' not in self.buf:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise RuntimeError('bench: ScummVM went away')
            self.buf += chunk
        line, _, self.buf = self.buf.partition(b'\n')
        return json.loads(line)

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(5)
            except subprocess.TimeoutExpired:
                self.proc.kill()


def run(bench, steps):
    for st in steps:
        if 'wait' in st:
            time.sleep(st['wait'])
        elif 'key' in st:
            k = st['key']
            code, ascii_ = KEYS[k] if k in KEYS else (ord(k), ord(k))
            print('key', k, bench.call('key', code=code, ascii=ascii_))
        elif 'move' in st:
            print('move', bench.call('move', x=st['move'][0], y=st['move'][1]))
        elif 'click' in st:
            print('click', bench.call('click', x=st['click'][0], y=st['click'][1], button=st.get('button', 1)))
        elif 'save' in st:
            print('save', bench.call('save', slot=st['save'], name=st.get('name', 'bench')))
        elif 'load' in st:
            print('load', bench.call('load', slot=st['load']))
        elif 'shot' in st:
            path = os.path.join(bench.out, st['shot'] + '.png')
            print('shot', bench.call('shot', path=path))


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    game, binary, labs, script = sys.argv[1:]
    b = Bench(game, binary, labs)
    try:
        run(b, json.load(open(script)))
    finally:
        b.stop()


if __name__ == '__main__':
    main()
