#!/bin/zsh
# resume.sh <slot> : waits for the daemon (started separately), boots past the logos and loads the slot
D=/private/tmp/claude-501/-Users-simonstark-AI-Projects-development-pointandtap/2ab47836-e45b-4986-bdee-75a4926704c1/scratchpad/proof
for i in {1..50}; do grep -q "bench up" $D/daemon.log 2>/dev/null && break; sleep 0.3; done
rm -f $D/.logpos
$D/g.py "[{\"wait\":4},{\"skip\":1},{\"wait\":2},{\"skip\":1},{\"wait\":3},{\"load\":$1},{\"wait\":6},{\"shot\":\"proof/resume-$1\"}]"
