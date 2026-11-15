# Grim Fandango: PointyClicky Edition

**The afterlife. Finally on point.**

Grim Fandango, played by pointing and clicking: no tank controls. Point at
something and Manny walks there and deals with it; click elsewhere and he
walks there. It plays the whole game, start to finish, the way the other
LucasArts adventures play.

It's the edition PointyClicky (https://pointyclicky.app) plays on iPhone,
but it's a project in its own right: a patch to ScummVM's Grim engine and a
data file, usable in any ScummVM build.

It starts from Tobias Pfaff's **Grim Mouse** (see CREDITS.md) and aims to
finish the job: every scene's hotspots right, every puzzle natural with a
pointer, no crashes, and proven by playing the whole game point-and-click
from a new game to the credits.

## What's here

| Path | What it is |
|---|---|
| `engine/grim_pointyclicky.patch` | the change to ScummVM v2026.4.0's `engines/grim` (`git apply` it in a ScummVM checkout) |
| `data/hotspots/*.set.hot` | the hotspots, one file per set: polygons in 640x480 game pixels per camera setup |
| `data/lab/` | patches to the game's scripts and costumes (`.patchr`), cursors and inventory images (`.tga`), and the compiled `mouse.lua` |
| `data/scripts/mouse.lua` | `mouse.lua`'s source |
| `tools/build-lab.py` | packs `data/` into `grim-pointyclicky.lab`, after checking every script patch fits your copy of the game (1.01 update included) |
| `docs/` | the recce, the plan and the notes |

## Build

```sh
python3 -I tools/build-lab.py --game <your Grim folder>   # -> build/grim-pointyclicky.lab
cd <scummvm v2026.4.0> && git apply <this>/engine/grim_pointyclicky.patch
```

Put the `.lab` where ScummVM finds its engine data and set `grim_mouse=true`
for the game.

## Licence

GPL-2.0-or-later (COPYING), like Grim Mouse and ScummVM.
