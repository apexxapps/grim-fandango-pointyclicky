#!/bin/zsh
# cycle.sh <slot> [nosave] : save to slot, quit, rebuild mouse.lua + lab, restart the daemon, load the slot
# Working folder: build/proof-bench (git-ignored): labs/, daemon.log, .logpos, observer files.
R="/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky"
T="$R/tools/proof"; W="$R/build/proof-bench"
if [ "$2" != "nosave" ]; then python3 "$T/g.py" "[{\"save\":$1,\"name\":\"proof $1\"}]"; fi
python3 -c "
import socket;s=socket.create_connection(('127.0.0.1',47123));s.sendall(b'\"quit\"\n');print(s.recv(100))" 2>/dev/null
cd "$R" && ~/Developer/pointyclicky-build/grimmouse/delua/luac -o data/lab/mouse.lua data/scripts/mouse.lua && python3 -I tools/build-lab.py || exit 1
sleep 1
rm -f "$W/daemon.log"
BENCH_DEBUG=$DBG nohup python3 -u "$T/daemon.py" > "$W/daemon.log" 2>&1 &
sleep 2
"$T/resume.sh" $1
