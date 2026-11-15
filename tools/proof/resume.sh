#!/bin/zsh
# resume.sh <slot> : waits for the daemon (started separately), boots past the logos and loads the slot
R="/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky"
T="$R/tools/proof"; W="$R/build/proof-bench"
for i in {1..50}; do grep -q "bench up" "$W/daemon.log" 2>/dev/null && break; sleep 0.3; done
rm -f "$W/.logpos"
python3 "$T/g.py" "[{\"wait\":4},{\"skip\":1},{\"wait\":2},{\"skip\":1},{\"wait\":3},{\"load\":$1},{\"wait\":6},{\"shot\":\"proof/resume-$1\"}]"
