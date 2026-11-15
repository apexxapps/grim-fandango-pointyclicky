#!/bin/zsh
# m.sh out a b c ... : montage proof shots (names without .png) at half size
P="/Users/simonstark/AI Projects/development/grim-fandango-pointyclicky/build/bench/proof"
o=$1; shift; f=(); for x in $@; do f+=("$P/$x.png"); done
n=${#f}; cols=$(( n < 3 ? n : 3 ))
montage $f -tile ${cols}x -geometry 320x240+2+2 "$P/$o.png" 2>/dev/null; echo "$P/$o.png"
