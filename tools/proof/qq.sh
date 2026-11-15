#!/bin/zsh
# qq.sh <slot> : save the proof game to <slot>, run proof/q.lua against it in developer mode (a separate observer run), print Q lines, restart the proof bench at <slot>
D=/private/tmp/claude-501/-Users-simonstark-AI-Projects-development-pointandtap/2ab47836-e45b-4986-bdee-75a4926704c1/scratchpad
$D/proof/g.py "[{\"save\":$1,\"name\":\"proof $1\"}]" >/dev/null
python3 -c "
import socket;s=socket.create_connection(('127.0.0.1',47123));s.sendall(b'\"quit\"\n');s.recv(100)"
sleep 1
echo '[{"wait":2},{"key":"ctrl"},{"key":"p"},{"wait":2}]' > $D/proof/q.json
cd $D && python3 run.py dq proof/q.lua proof/q.json --load $1 >/dev/null 2>&1
grep -a "Debug: Q" "/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky/build/bench/scummvm.out"
$D/proof/cycle.sh $1 nosave >/dev/null
