#!/bin/zsh
# cycle.sh <slot> : save to slot, quit, rebuild mouse.lua + lab, restart the daemon, load the slot
D=/private/tmp/claude-501/-Users-simonstark-AI-Projects-development-pointandtap/2ab47836-e45b-4986-bdee-75a4926704c1/scratchpad/proof
R="/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky"
if [ "$2" != "nosave" ]; then $D/g.py "[{\"save\":$1,\"name\":\"proof $1\"}]"; fi
python3 -c "
import socket;s=socket.create_connection(('127.0.0.1',47123));s.sendall(b'\"quit\"\n');print(s.recv(100))" 2>/dev/null
cd "$R" && ~/Developer/pointyclicky-build/grimmouse/delua/luac -o data/lab/mouse.lua data/scripts/mouse.lua && python3 -I tools/build-lab.py || exit 1
sleep 1
rm -f $D/daemon.log
cd $D && BENCH_DEBUG=$DBG nohup python3 -u daemon.py > daemon.log 2>&1 &
sleep 2
$D/resume.sh $1
