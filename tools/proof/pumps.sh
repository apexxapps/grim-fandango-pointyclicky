#!/bin/zsh
# pumps.sh <prefix> <n> : the four pumps' tip brightness per frame (lower = piston out)
cd "/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky/build/bench/proof/burst"
for i in $(seq 0 $(($2-1))); do f=$(printf "$1%02d" $i).png
  printf "%02d" $i
  for g in 22x14+454+113 22x14+462+137 22x14+556+113 22x14+558+138; do printf " %5.0f" $(magick $f -crop $g +repage -colorspace gray -format "%[fx:mean*1000]" info:); done; echo
done
