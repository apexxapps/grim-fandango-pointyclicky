#!/usr/bin/env python3
"""beaver.py <manny x> <manny y> [throw] : the beaver dam's bone and extinguisher, by the player's gestures.
With 'throw', first a tap on the river of tar (a bone in hand: Manny throws it). Then a tap on Manny (the
coat), the coat's left third until the fire extinguisher shows (read off the screen: its red body), the
middle (take it), and a press held over the tar (moment 16: U held) until the game's dive is over.
Every step is one of the bench's pointer steps; the screen is only looked at, as the player would."""
import json, socket, subprocess, sys, time
R = '/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky'
TMP = R + '/build/proof-bench/coat.png'
TAR = [380, 400]


def bench(steps):
    s = socket.create_connection(('127.0.0.1', 47123))
    s.sendall((json.dumps(steps) + '\n').encode())
    d = b''
    while True:
        c = s.recv(65536)
        if not c:
            break
        d += c
    return d.decode()


def red_share():
    bench([{"shot": "../proof-bench/coat"}])
    out = subprocess.run(['magick', TMP, '-crop', '320x300+160+0', '+repage', '-fx', '(r>0.6 && g<0.25 && b<0.25) ? 1 : 0',
                          '-format', '%[fx:mean]', 'info:'], capture_output=True, text=True).stdout
    return float(out or 0)


def log(*a):
    print('%.2f' % (time.time() - T0), *a, flush=True)


T0 = time.time()
mx, my = int(sys.argv[1]), int(sys.argv[2])
def green_at(x, y):
    """Manny's suit is drawn here (his green, read off the screen)."""
    bench([{"shot": "../proof-bench/coat"}])
    out = subprocess.run(['magick', TMP, '-crop', '24x40+%d+%d' % (x - 12, y), '+repage', '-fx',
                          '(g>r*1.15 && g>b*1.3 && g>0.2) ? 1 : 0', '-format', '%[fx:mean]', 'info:'],
                         capture_output=True, text=True).stdout
    return float(out or 0)


def pointer_seen(x=600, y=440):
    """The pointer is drawn (it hides in cut scenes): bright pixels round it."""
    bench([{"shot": "../proof-bench/coat"}])
    out = subprocess.run(['magick', TMP, '-crop', '20x20+%d+%d' % (x - 10, y - 10), '+repage', '-colorspace', 'gray',
                          '-fx', 'u>0.75 ? 1 : 0', '-format', '%[fx:mean]', 'info:'], capture_output=True, text=True).stdout
    return float(out or 0) > 0.03


if 'throw' in sys.argv:
    bench([{"click": TAR}, {"move": [600, 440]}])
    log('throw')
    for i in range(60):   # the throw's cut scene: the pointer goes ...
        if not pointer_seen():
            break
        time.sleep(0.1)
    log('cut scene')
    for i in range(80):   # ... and comes back when Manny can act again
        if pointer_seen():
            break
        time.sleep(0.1)
    log('pointer back')
    time.sleep(float(sys.argv[sys.argv.index('throw') + 1]))
bench([{"click": [mx, my]}])
log('coat')
time.sleep(2.2)
for i in range(8):
    v = red_share()
    log('red %.3f' % v)
    if v > 0.08:
        break
    bench([{"click": [80, 240]}])
    time.sleep(1.3)
else:
    sys.exit('no extinguisher seen')
bench([{"click": [320, 240]}])
log('take')
time.sleep(1.1)
bench([{"press": TAR}])
log('press')
for k in range(4):
    time.sleep(1.5)
    bench([{"shot": "proof/bv-%d" % k}])
time.sleep(float(sys.argv[-1]) if sys.argv[-1].replace('.', '').isdigit() and 'hold' in sys.argv else 1.0)
bench([{"release": TAR}])
log('release')
time.sleep(3)
bench([{"shot": "proof/bv-end"}])
