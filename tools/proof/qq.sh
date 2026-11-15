#!/bin/zsh
# qq.sh <slot> [lua] : save the proof game to <slot>, run <lua> (default build/proof-bench/q.lua) against it
# in developer mode (a separate observer run, never the proof game), print its "Q" lines, restart the proof bench at <slot>
R="/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky"
T="$R/tools/proof"; W="$R/build/proof-bench"
Q=${2:-$W/q.lua}
python3 "$T/g.py" "[{\"save\":$1,\"name\":\"proof $1\"}]" >/dev/null
python3 -c "
import socket;s=socket.create_connection(('127.0.0.1',47123));s.sendall(b'\"quit\"\n');s.recv(100)"
sleep 1
echo '[{"wait":2},{"key":"ctrl"},{"key":"p"},{"wait":2}]' > "$W/q.json"
python3 "$T/observe.py" dq "$Q" "$W/q.json" --load $1 >/dev/null 2>&1
grep -a "Debug: Q" "$R/build/bench/scummvm.out"
"$T/cycle.sh" $1 nosave >/dev/null
