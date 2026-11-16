# The proof playthrough (PLAN.md phase 5, item 2)

*Started 15 Nov 2026. In progress: from a new game through Year 1 and into
Year 2 (Seaman Naranja done). Not yet at the credits. Resume from save 158
(build/bench/saves/grim158.gsv; see "Resume here" at the end).*

**The bar.** The 1998 game from a new game to the end credits on the Mac
bench, using only what a player on the phone has: tap, two-finger tap (look),
double tap (run), press and hold where moments.md says, tap Manny for the
coat and the coat's thirds, Skip (Esc) for cut scenes only. No keyboard keys,
developer mode off, no jumps. Saves made along the way and resumed from after
a fix. Where something can't be done by pointer it is fixed under the laws and
that spot proven again.

**How it's run.** ScummVM built with the edition (the bench binary,
`~/Developer/pointyclicky-build/grim-bench`) held open by a small driver that
sends the bench's own steps one at a time (tools/bench.py's `Bench`: clicks,
right clicks for two fingers, two clicks 120 ms apart for a double tap, Skip
as the rig's Esc). Developer mode is off in the proof game. Reading the game's
state (a flag, Manny's position) was done only from a **separate** run of a
save in developer mode, never in the proof game itself; those runs are noted.
Outlines were drawn on screen (BENCH_DEBUG) twice, to see a scene's
hotspots, with no input sent in that mode.

**The solution followed.** Jeff "CJayC" Veasey's *Grim Fandango FAQ/
Walkthrough* v1.7 (1 Dec 1998, GameFAQs; mirrored at
https://www.gameboomers.com/wtcheats/pcGg/GrimFanJeff.htm), Year 1 to Year 4.

**Screenshots.** `build/bench/proof/NNN.png` (git-ignored: they are the
game's own art, which the repo never holds, law 7). The numbers below are
those files. Saves: `build/bench/saves/grimNN.gsv`, slots 50 on.

---

## Fixes

Each: where, what was wrong, the fix, the shots. Outline coordinates are
640x480 game pixels.

1. **ga, setup 1 (ga_entha), the big door (gatx121).** Its outline ran a strip
   along the whole bottom of the screen (x 0-563, y 460-478) over the
   'elevator' walk path; objects are hit before walk paths, so a tap on the
   floor near the bottom walked Manny to the big door. The strip is cut; the
   door keeps the right wall. Shots 028, 029.
2. **ha, setup 0 (ha_elvos), the garage elevator (hatx161).** Its outline
   took in the red carpet and the left wall (x 110-513, y 37-433), so a tap on
   the carpet in front of the main lift sent Manny down to the garage. Redrawn
   round the lattice door (x 157-214, y 95-395). Shot 037.
3. **ha, setup 0, the hole punch (hatx131, Eva's desk in the foreground).**
   Reached up across the carpet to y 365; its top now follows the desk's front
   edge (y 425 in the middle). Shot 040.
4. **co, Copal's computer: a dead end (the blocker of the run so far).** After
   a reply was set (or Esc), every tap was swallowed and Manny was stuck in
   Copal's office for good. co.lua's Grim Mouse patch switches the pointer to
   its dialogue mode when the computer opens and only Grim Mouse's own
   `mouseSelect` switched it back; since the computer is worked by its own keys
   (moments.md line 11) nothing did. mouse.lua: `co.computer.stop_interface`
   (the game's own way out, both for U and Esc) now puts the pointer back
   first (`SwitchControlMode(0)`), and on load a save made while stuck is freed
   (mouse.lua runs again after every load). Shots 062-064 (stuck), 066 (that
   save, loaded: a tap on the window takes Manny out).
5. **le, setup 0 (le_alloh), the hanging rope of ties (letx001).** A small box
   beside the ties (x 268-293, y 298-365); a tap on the ties as drawn did
   nothing, so there was no way down. Widened over the ties to the bottom of
   the screen. Shots 068, 069.
6. **mo, setup 3 (mo_cornr), the deck of playing cards (motx094).** A sliver
   under the table's edge; a tap on the box of cards as drawn walked. Redrawn
   round the box and the cards (x 250-358, y 236-286). Shots 093, 094.
7. **ha, setup 3 (ha_evaws), the hole punch.** No outline on this angle (the
   audit's depth test called it hidden), but it's the saucer on Eva's desk in
   plain view at the game's own point, and the cards are punched from here.
   Outlined. Shots 101, 104.
8. **Engine: a tap on Manny (the coat).** The test was his feet-to-head line
   with a quarter of his height either side, so in a near shot it took in
   things beside his head: the hole punch over his shoulder opened the coat
   (shot 102). Now `HotspotMan::tapOnManny`: that box, and within it Manny as
   drawn this frame (his costume's box, as characters are found), at head
   height only his head (a sixth of his width either side), and an outlined
   thing nearer the camera than Manny wins. The old box stays the fallback when
   he isn't drawn. Proven: the hole punch (105), the coat on Manny (106), the
   roof (272-274: the box is used only within the line box, because while the
   game walks him by script his drawn box can lag).
9. **lo, setup 2 (lo_elews), the front doors (lotx015).** Reached left over
   the dark corner to x 376, over the 'side1' walk path; a tap there took Manny
   out into the street instead of to the tube room's side. Cut back to the
   doors. Shot 130.
10. **lo, setup 0 (lo_tubws), the tube room's door (lotx009).** Cut away on
    its right by a diagonal: with Manny in the doorway the only parts left to
    tap were round his head (the coat). Squared to the door's frame (x
    129-262). Shots 180, 181.
11. **do, Domino's office, setup 1 (do_winws): the window (dotx161), the only
    way out.** No outline on any angle: the office's Lua table is `dom`, not
    `do`, so tools/inventory.py never matched its objects (the audit says
    "objects: 0" for do). A tap on the window walked. Outlined round the glass.
    Shots 249-251. *Tools item:* the audit's set-name match misses sets whose
    table isn't named after the set file; worth a pass for others.
12. **rf, setups 1 and 2, the pigeons (rftx021).** Outlined over the whole
    roof, so every tap on the roof walked Manny at the pigeons. Cut down to the
    flock as it sits on each angle. Shots 268-271.

13. **sp, the spider web clearing: no way back out.** Both of Grim Mouse's
    'out' walk paths walked Manny to (-5.70, 6.62), a point in the signpost
    fork's own coordinates, outside this set, so he stopped short and never
    reached the game's way out (`sp.sg_door`, the sg_box sector at -0.86,
    -0.48). Pointed at the door's own position. Shots 329-331 (stuck, then out
    to the fork).

14. **Engine: a character or vehicle behind the camera.** In tr (setup 2) the
    parked Bone Wagon stands behind the camera, and its costume's box on screen
    came out as a mirror image over the right of the screen, so a tap on the
    wheelbarrow went to the Bone Wagon "as drawn": Manny got in and drove off
    (shots 346-348; the tall orange box in 355). An actor behind the camera
    (`HotspotMan::cameraDepth` of its position <= 0) is no longer found as drawn
    (`liveActor`, and the vehicles' `onActor`). Shot 356: the box gone, the
    barrow's own box left; a tap on the barrow takes it.
15. **tr and ac: the wheelbarrow's pull, and the anchor room crawl, never
    ended** (a dead end: the barrow can't be parked between hoses). Grim
    Mouse's tr.lua and ac.lua patches had changed the 1998 loops to `while
    <key held> or find_script(tr.linearMoveMinus) and ...` for its linear mode;
    the edition retired that mode from mouse.lua (moments.md 6 and 7), and
    `find_script(nil)` answers true, so a pull ran on after the key was let go,
    the release had already set the walk rate forward, and Manny pushed the
    barrow past the push limit and off down the road ("That's the kind of hike I
    just don't need"; shot 357, from save 88). The 1998 keys did the same (an
    observer run, one Down press). The tr.lua and ac.lua patches now carry the
    1998 loops (recompiled from the decompiled patched script with only those
    two conditions changed; the round trip decompiles to the same code), and
    mouse.lua gives saves made before this a stand-in for the names (a function
    that never runs, so find_script answers nil). Proven from save 88 (made
    before the fix): pulled, stops, stays (358); in a new game both scripts load
    (observer run). The crawl wasn't replayed (Year 2).

16. **sg, setup 1 (sg_sgnha), the sign post (sgtx050).** The outline sat to the
    right of the post (x 423-451); the game's own point for it (419,358, base
    417,381) was outside it, so a tap on the post as drawn walked Manny up to it
    and did nothing. Redrawn round the post (x 402-436, y 336-388); in hand.txt.
    Shots 372 (the walk), 373-374 (taken up).

17. **Engine and mouse.lua: a held item used on its own** (question 1, decided
    by Simon 15 Nov 2026). With an item in hand a tap on Manny put it away, and
    using it on its own needed Grim Mouse's hidden two-finger tap on the floor.
    Now a tap on Manny with an item in hand is the 1998 U with nothing targeted
    (`system.mouseUseHeld`: `Sentence("use", item)`, the last USE branch of
    _controls.lua; the engine's tap-on-Manny calls it instead of sending P);
    putting it away is the game's P, which the app is to send for a swipe up
    (on the bench a P key stands in for the swipe); the two-finger floor use is
    gone from `just_walk`, so two fingers on the floor only walk. Re-proven:
    save 77 (gs, the mouthpiece bonded, in hand): a tap on Manny, "Wow, that
    made a perfect impression of my teeth" (q1-d to q1-f); P puts it away and
    the next tap on Manny opens the coat (q1-g to q1-i); with the eggs in hand
    two fingers on the floor walk and use nothing, a floor tap walks (q1-j to
    q1-n); save 78 (already molded): "Yep. A perfect fit." (q1-a to q1-c).
    Save 100 (na): the sign picked up by a tap, planted off the spot by a tap
    on Manny (q1-p, q1-q), picked up, walked to the spot, planted by a tap on
    Manny: it spins, the trapdoor, "¡Lotería!" (q1-u to q1-y).

18. **na, setup 1 (na_intha), the sign post in the clearing (natx002).** Its
    outline was a strip right across the screen (x 0-639, y 255-343, the band
    the sign can be planted in), so with the sign planted, a tap on the empty
    floor anywhere in that band lit the cursor and took the sign up from across
    the clearing (save 99: a tap at 560,270, shots 418-420). The sign is the
    game's own `signpost` actor, moved wherever Manny plants it, so mouse.lua
    now links na.signpost to it (`LinkHotspotActor`, as the characters and
    vehicles are): it's found where it stands (law 3), the outline only when
    it isn't drawn. Proven from save 99: the same tap walks, the cursor stays
    bone (421-422); a tap on the sign as drawn takes it ("tap on sign post (as
    drawn)", 425-426).

19. **lm, setups 2 and 3 (lm_gngms, lm_nolim), the bottle on Velasco's desk
    (lmtx115).** Its outline was a band over the whole dock (x 70-639, y
    160-450), Velasco and Manny's own floor included, so a tap on Velasco took
    the bottle ("tap on bottle": Manny walks over and remarks) and his
    conversation could not be started. Redrawn round the bottle on the desk (x
    512-560, y 274-306); in hand.txt. Shots 598-599 (the bottle taken), 600-601
    (a tap on Velasco: his conversation).
20. **cn, the roulette room: no way back out to the bar** (a dead end). A tap on
    the door (cntx249) did nothing. The game's `Sentence("walkOut")` walks first
    to a closed door's use point, and cn's (-0.64, 0.35) is off the floor: the
    room's walk sectors are one narrow walkway from Charlie's booth to the door
    corridor, so Manny stopped at its corner (-0.175, 0.65) and the sentence gave
    up (read in observer runs of saves 123 and 124). The 1998 player left by
    walking into the door's box (ci_box), which runs the door's own walkOut.
    mouse.lua's `walk_and_do`: when the walk to a closed door's use point fails,
    Manny walks (or runs) on to the door's out point, through its box, and the
    game does the rest; if no box took it, the door's own walkOut is called.
    Proven from save 124 (Manny stuck at the corner: a tap on the door, out to
    the bar, 642) and save 123 (a double tap from the booth, 643). Shots 635-641
    (stuck). *Tools item:* other doors whose use point is off the floor would
    have failed the same way; the fix covers them all.

21. **The forklift in the elevator (moment 2; de): it could not be lined up,
    got off or worked from its lever side** (a dead end for the union card).
    Seen from above in the elevator, the forklift's drawn box covered most of
    the floor and the grating: (a) every tap on the grating, where it must be
    driven to jam the shaft, was "on the vehicle" (U, get off: shots 732, 747);
    (b) a tap the forklift was already "at" did nothing, so it could not be
    turned to line up with the lanes (fork_box2/3, 0.07 wide); (c) the drive
    scale stopped it 0.3 short, wider than the lanes (748-749); (d) from the
    lever side, a tap took the forklift (get on), never the fork lever, which the
    game makes touchable there (de.forklift_actor.monitor_objects). Fixes, in
    the engine (hotspotman.cpp) and mouse.lua: getting off is a tap on the seat,
    where Manny sits (and anywhere on it while jammed in the shaft); the forklift
    is found by the outline of its body (fork tips to rear, floor to mast top),
    not its screen box; a tap it is already at turns it on the spot to face the
    tap (the arrows only); the forklift's scale is now 0.06 to arrive (0.08 for a
    way out); and in mouse.lua a tap on the forklift works the lever when the
    game has made the lever the touchable one (Manny at the lever's side, not
    driving). Proven: turned (739, 743), lined up (750), off by the seat (754,
    758), button, on, pushed through the window: the elevator jams on the forks
    (757, save 142), round to the lever side (764), a tap: the forks up, the
    hidden floor (765, save 144), into the hallway (768) and the suitcase (771-
    773). Bench: build/proof-bench save 139-146.

22. **bi, setup 0 (bi_clbws), the Blue Casket's microphone (bitx415).** Its
    outline ran on past the stage over the floor and the table to its right (to
    x 294, y 344), so a tap on the floor in front of the stage walked Manny up on
    stage to the microphone (the poetry reading's lines: shot 800). Cut back to
    the stage (x 252 at most); in hand.txt. Shot 802 (the same tap walks).
23. **Engine: the Blue Casket stopped the game** (a dead end: ScummVM quit).
    During Lola and Olivia's scene at the back of the club, TinyGL's draw-call
    memory ran out ("Allocator out of memory: couldn't allocate more memory from
    linear allocator", an error() that ends the engine; shots 805-808,
    reproduced three times from save 147). Measured: the full club takes about
    4.0 MB a frame, the close-up 5.75 MB; TinyGL's default is 5 MB.
    gfx_tinygl.cpp now gives Grim's context 16 MB (createContext's own
    drawCallMemorySize argument). Proven from save 147: the scene plays through
    (809-812). The phone uses the software renderer too, so this was a crash on
    the phone as well. *Bench aid:* a walk tap now logs the sector it lands in
    ("walk to floor_5 (x, y, z)").

(NB `tools/hotspots.py` rewrites data/hotspots from the traces. Checked 15 Nov
2026: a re-run undid most of these (a trace that passes its checks always won).
Now **data/hotspots/hand.txt** lists every outline fixed by hand (set, setup,
id), and hotspots.py keeps those lines as they are, or keeps them off when
taken off by hand; a re-run changes nothing but the order of two identical
lines. Every new hand fix needs its line there.)

## Tools items found on the way

- **"Ten script patches don't match the player's copy": wrong, they all
  apply (checked 15 Nov 2026, third session).** _cut_scenes, _options, _system,
  al, at, bd, bk, de, rf and th are among the scripts LucasArts' 1.01 update
  replaced: gfupd101.exe carries a DATA005.LAB (in a scrambled cabinet), and the
  engine reads it ahead of DATA000-004 (engines/grim/update; the engine refuses to
  start without gfupd101.exe, and the app keeps it: Trim.engineReads). Grim
  Mouse's patches were made against those 1.01 scripts, so they fit. The check
  that raised it, like tools/grimfiles.py and tools/inventory.py, read DATA000-004
  only. Proven in the engine: a boot with `BENCH_DEBUGFLAGS=patchr` logs "Patch for
  X successfully loaded" for all ten (59 patches at boot, the rest load with their
  files; none skipped). So no player ever lost these patches, and nothing in
  those scenes changes. None of the ten was ever edited by the edition (all as
  imported in 1df957c): its moments are in mouse.lua and the engine.
  What the ten do (Grim Mouse's changes, decompiled against the 1.01 scripts): at
  switches the pointer mode around the tunnel ride's remote; de walks the forklift
  with Actor.walkto and stops it nearer (0.05); bd waits for the coat to close
  before the extinguisher and moves a beaver and a walk point; al makes the
  alley's dummy door touchable while it's live; rf names the dish and makes the
  nest touchable once the pigeons are gone; bk and th name the bottle and the
  grinder for the coat, and th starts the snow machine's pickUp; _options keeps
  the pointer mode across pause and the menus; _cut_scenes only renumbers lines.
  **Made loud:** (1) the engine: `wrapPatchedFile` warns whenever a file has a
  patch and none fits ("Grim: no patch fits al.lua (size 9079): it plays
  unpatched!"), whatever the debug flags; proven with a lab whose al.lua.patchr
  had a wrong target. (2) `--debugflags=patchr` (and every Grim channel) prints
  again: `Debug::debug` asked for `channel | Info`, which names no channel since
  channels became ids (debug.cpp, the same bug `scripts` had). (3) tools:
  grimfiles.Game reads the update's DATA005.LAB as the engine does
  (`update_files`), and build-lab.py now needs the game folder (`--game` or
  GRIM_GAME) and stops if any patch fits no file the engine would read (all 70
  fit; a spoiled target is caught). inventory.py reads the scripts the engine
  runs too (it had been auditing the 1.0 versions of those ten). bench.py:
  `BENCH_DEBUGFLAGS` turns on engine channels.
  **Re-checked on the bench from Simon's saves (shots p1-*):** the tunnel ride
  (17): forward to the albinizod (blocked), back up, the catwalk (U), Glottis on
  the wagon (the remote, I). The forklift (14): on by a tap, into the elevator
  (de), about it, back out to the cellar, off by a tap. The extinguisher (27):
  the coat, one to the right, out; held, it sprays; lifted, it stops; a quick tap
  walks. Two notes, not faults: a tap on the wagon's front legs, more than 1.5
  units down the tunnel from it, drives there rather than working the remote
  (tunnelTap's rule); and in save 14 Manny stands at the forklift's seat, so a
  tap there is a tap on Manny (the coat): the forklift's body gets him on.
- An observer run (developer mode) of a save made while holding the
  wheelbarrow drifted within seconds of loading, so its numbers weren't the
  proof game's; read state right after the load (`OBS_WAIT`).

---

## Physical checks for Simon

*Asked by Simon (15-16 Nov 2026): "is everything physically doable?" The bench
taps exact game pixels with machine timing; on the phone the whole screen is a
trackpad: a finger slides the pointer, then taps. Sizes are in 640x480 game
pixels, and roughly on a 6.1" iPhone (1 game px = about 2.5 pt; Apple's
comfortable touch target is 44 pt, about 18 game px, but here the finger aims
the pointer, so the limit is how finely a slide places it, not the fingertip).
Each has a save made just before it in build/for-simon (README.md lists them).*

P1. **The tree pump (tr, Year 1).** Target: a hose strip under the barrow's
    path, about 0.1 units long (the barrow's travel crosses each in some 0.1-0.15
    of rail, a few px on screen), but the player taps along the rails (a big
    target) and the timing is what matters. Window: leave a hose during the
    0.5 s before its partner pump strikes; a pull leaves the hose 0.35-0.5 s
    after the tap (the walk winds up), a push about 0.75 s after. So the tap
    lands in a window of about 0.35 s, read off the pistons on the tree.
    Gesture: tap along the rails (push/pull), as moments.md 6. Saves 36 (before
    the left pair), 37 (left pair set). **Likely too hard** (the bench needed a
    second try with a stopwatch on the pistons, and a person has to work out
    which piston is which). It is the 1998 puzzle and the 1998 timing; what the
    pointer adds is the wind-up (0.35-0.5 s, varying) between tap and leaving
    the hose, which a key press also had. Suggested fix within the laws: none in
    the rule itself (law 2); on the phone, a press held on the rails could be the
    1998 key held (as the extinguisher's hold is), so the barrow moves while the
    finger is down and stops when it lifts: the player times the lift, which is
    exactly the original's timing with no wind-up guesswork. For Simon.
P2. **The beavers (bd, Year 1).** Target: the tar (setup 1: 303-634 x 109-253,
    330 x 145 px, about 825 x 360 pt): easy. Window: about 10 s from the throw to
    the beaver's dive, in which the pointer comes back (~2 s), the coat opens
    (~2 s; a tap in its first second or two is ignored), one step per item to the
    extinguisher (~2.3 s each), take it (~3.5 s), then press and hold (0.4 s to
    count as a hold) until it freezes. Gesture: tap the tar with a bone (throw),
    tap Manny (coat), the coat's thirds, press and hold over the tar. Save 38.
    **Tight:** with the extinguisher one step from the bone it fits with 1-2 s
    spare; two steps away it doesn't. The game helps: the coat opens on the item
    last put away, so after the first try the extinguisher is the first thing
    shown. A miss costs nothing (throw another bone). Suggested fix within the
    laws: none needed; say it in the hints ("have the extinguisher last in the
    coat").
P3. **The waiter (hk, Year 2).** Target: the pantry doors (36 x 164 px, about
    90 x 410 pt): easy. Window: he comes every 20-27 s and is inside some
    seconds; close the doors by a tap while he's in, then the scythe on them.
    Gesture: tap, then the coat, scythe, tap the doors. Save 39. OK (a miss
    waits for his next trip).
P4. **The forklift's lanes (de, Year 2).** Target: lining the forks up with a
    lane in the elevator (fork_box2 and fork_box3, 0.07 units wide: from above,
    setup 1, 6 x 11 px, about 15 x 28 pt); the forklift arrives within 0.06 of
    a tap (fix 21) and a tap it's already at turns it to face the tap. Window:
    after the button, the elevator moves; the forklift must be driven through
    the window and pushed at the hidden floor (several seconds). Gesture: taps
    to drive and turn, a tap on the seat to get off. Save 40. **Likely too
    hard:** a tap has to land within about 3 px either side of a lane's line, by
    sliding the pointer; on the bench it took several turns (739-750). Suggested
    fix within the laws: a tap within some 12 px of a lane goes to the lane's
    own centre (the lanes are the game's sectors, fork_box2/3, law 1), so the
    finger only has to be near it; the drive itself stays the game's keys.
P5. **The sign in the clearing (na, Year 1).** Target: the spot (na.rubacava_point,
    within 0.6 units: about 16 px on screen, about 40 pt). Window: none. Gesture:
    tap the floor to walk there, tap Manny (plant). Save 41. OK, but the spot is
    unmarked (it's the riddle); fine as the 1998 puzzle.
P6. **Naranja's bottle (si, Year 2).** Targets: the fridge, the crisper (206 x
    246 px), the bottle (setup 1: 169 x 130 px): easy. Window: the fridge's motor
    starts 10 s after the fridge opens; Toto then yells and looks away for about
    5 s plus his line; the baster on the bottle must be used before he shuts the
    fridge (from the crisper opening to that, some 15-20 s; the bench used 13 s,
    coat included). If used early, the game waits for the distraction itself.
    Gesture: taps, the coat (two steps at most), a tap on the bottle. Save 42. OK.
P7. **The blimp desk's metal detector (sl, Year 2).** Target: the detector's
    box on the floor (the sector detector_box: a slanted 70 x 33 px patch, about
    175 x 80 pt), or any floor beyond the gate (Manny walks through it). Window:
    10 s from the end of the drink to the burp. Gesture: the coat, the liqueur,
    tap Manny (drink), swipe up (put it away), tap the floor beyond the gate.
    Save 43. OK on time (about 3-5 s needed). **A snag a person will hit:** a tap
    on the gate itself is the game's own `sl.gate.use`, which walks Manny to
    (0.154, -0.297), 0.003 short of the box, so nothing happens and the time
    runs out (the bench did exactly that: shots i1-i9, k3-k9). In 1998 the same
    U stopped short too; players walked through. Suggested fix within the laws:
    none in the scripts; the hints should say "walk through it". For Simon: or
    the gate's use point could be read as "walk through" (it's 3 mm off the box),
    which would be a bent law 2.
P8. **The bench's other tight spots, checked and fine:** the rope throw on the
    ledge (a tap anywhere in the sky), the extinguisher's hold (0.4 s anywhere
    on the tar), the roulette room's door (fix 20), the bridge lever (wait for the
    bridge), the dialogue rows (21 px apart, about 52 pt).

## Questions for Simon

1. **Answered (Simon, 15 Nov 2026): a tap on Manny uses the held item on its
   own; a swipe up puts it away (fix 17).** The question was:
   **Using a held item on Manny himself** (the mouthpiece, for the dental
   impression: in 1998, U with nothing in front of him). A tap on the floor
   walks; a tap on Manny puts the item away. What worked is Grim Mouse's
   binding: **a two-finger tap on the floor with the item in hand walks there
   and uses it** (`just_walk`'s button 2 then `Sentence("use", held)`). That
   bends law 4 (two fingers = look), and nothing on screen says so. Options:
   keep it; or two fingers **on Manny** with an item in hand = use it on
   himself (Manny is the coat already, so it's "his" spot); or leave as is
   and say it in the hints. The run used the existing binding (shot 306).

---

## The run (notes; each line: what was done by pointer, the shots)

### Year 1: El Marrow

- **mo, Manny's office.** Tap the tube: the work order message (002-003).
  Tap the door (010). NB a tap on the floor just behind him opened the coat:
  he's very tall in this angle (006); fixed by fix 8.
- **ha.** Double tap the front-desk floor (runs, 012); tap the garage lift (013).
- **ga, the garage.** Run in, run to the shed corner, tap Glottis's door
  (014-016). Glottis by tapping lines: "Hey, you a driver?", "I'm Calavera",
  "Looks like I need a new driver", "You want to be my replacement driver?",
  "Come on, Glottis", "You're not too big..." (017-024). The work order (025).
  Save 50. Back to the lift (fix 1, 027-031).
- **ha.** Coat, the work order, tap Eva: Copal won't see you (042-045)
  (fixes 2, 3).
- **lo, os, st, al.** Out to the street and the alley (052-055). Tap the rope
  of ties: Manny climbs to the ledge (056-058). Tap Copal's window (059).
- **co.** Tap the computer; tap "Ah, cripes, Eva! Just sign it yourself"
  (reply 5; 060-062). Stuck (fix 4); out of the window (066). Down the ties
  (fix 5, 069).
- **st, rp, os, lo, ha.** Back in and up (075-078). Coat, work order, tap
  Eva: she signs it (079-080). Cut scenes to the Land of the Living (081-083).
- **lr, the diner.** Tap Manny: the scythe (084). Tap the body: the soul, and
  back to the garage (085-089). Save 52.
- **mo.** The playing cards on the side table (fix 6, 093-099).
- **ha.** Cards on the hole punch: one punched card (fixes 7, 8; 105-108).
  Save 55.
- **lo.** The demon's complaint about the tubes plays on the way out (111-112).
- **fe, the festival.** The clown: "Practicing what?", "Twist me up one of
  them", "Bet ya can't do a cat", "A dead worm": a balloon; again, "My kid
  wants another balloon animal", "...any more dead worms?" (113-125). Save 56.
- **pk, the packing room** (fix 9 on the way). Coat: one balloon on the blue
  nozzle, the other on the red: two full balloons (132-140). Save 58.
- **mo.** Each full balloon on the message tube (the coat's thirds to choose,
  148-155). Save 60.
- **tu, the tube room.** Tap the dead bolt (locks it open, 170). The
  repairman: "Who would do a terrible thing like this?", "Well, I gotta
  split": he hands over the fire extinguisher and shows Manny out (171-178).
  Save 61.
- **tu again** (fix 10). Tap the wheel: the booth opens (183). Coat, the
  punched card on the red tube: Domino's message caught; Meche (184-189).
  Save 62. "Excuse me, but I have to go straighten this mess out" (190).
- **ha.** Copal's door; down the hall: the funny-bones cut scene, Manny fired,
  locked in Glottis's shed (191-201). Save 63.
- **gs.** Tap the door: "getting out and getting even", "the DOD runs a
  crooked game", "blow the lid off": to the LSA (202-208).
- **hq.** Salvador: "Okay, I'm in", "messenger", "pigeons from the roof",
  "I'm off" (211-216). Save 64. Tap the lift: out to the alley (219-221).
  Save 65.
- **fe.** The clown: "My kid wants another balloon animal", "A cat": the cat
  balloon (223-229). The bread in the tent (230).
- **al, le.** Up the ties (save 66). Domino's window on the corner angle (236).
- **do, Domino's office.** The speed bag three times; the mouthpiece off the
  floor (239-244). The drawer: opened, then the coral (246-248). The window
  back out (fix 11, 251). Save 69.
- **le.** The loose end: Manny coils and holds the rope; tap Manny: the coat
  (moments.md 17's I), the coral: tied on (258-260). Save 71. The grappling
  hook, then a tap on the sky: thrown, caught (262-263). Save 72. Tap the
  rope: across. The ladder (moment 10): a tap higher up, he climbs to the roof
  (264-266).
- **rf, the roof** (fix 12). Coat: the cat balloon on the dish, then the
  bread: the pigeons go (270-283). Save 75. The nest: the eggs (284). Back to
  the ladder by the roof's 'back' path, the rope, the ties down (286-288).
- **al, ga, gs.** The big door into the garage (291); across to the corner,
  Glottis's door (292-300). Coat, the mouthpiece on the Fill-A-Dent (304); a
  two-finger tap on the floor with it in hand: Manny bites it (306; question 1).
- **al, hq.** The blue eye in the alley (311). The eggs on Salvador (313). The
  mouthpiece on Eva (317): Manny's papers, cut scenes (318).
- **The Petrified Forest** (319). Save 80.

### Year 1: the Petrified Forest

- **sm, sg.** Down the path ('next'): Glottis rips out his heart and throws it
  into the forest (320-321). Save 81.
- **sp, the spider web.** The path at the fork (322). The pile of bones: Manny
  takes one (325); a tap on the web with it: the bone sticks (326); coat, the
  scythe, a tap on the web: the heart flies out (327-328). Save 82. Back out
  (fix 13, 329-331).
- **sg.** The heart on the ground by Glottis (332); held, it can't go back in
  the coat ("put away" is refused); a tap on Glottis puts it back in (335-336).
  The Copal/Domino cut scene; in the Bone Wagon (337). Save 84.
- **The Bone Wagon (moment 1).** A tap on the way to the tree pump: driven
  there by the game's route (338). Save 85.
- **tr, the tree pump.** The wheelbarrow, tapped where it's drawn (the
  outline over the whole rails is not used while the barrow is live: 339-340).
  Pushed and pulled along the rails by taps (341-343). Save 87.
- **tr, second session (15 Nov 2026).** A tap on the barrow took the Bone Wagon
  behind the camera (fix 14). A pull never ended (fix 15). Then the pumps, by
  the walkthrough's way, which is the game's own rule (tr.hose_watch: a hose
  under the barrow stops its pump; when the barrow leaves it, the pump takes the
  beat of that moment; tr.pump_timer_and_checker strikes the pump whose beat
  comes up, every 500 ms, and tr.beat during the 500 ms before a pump's strike
  is that pump's beat). So: park on a middle hose, and leave it in the half
  second before its partner strikes. Read off the screen: the four pistons on
  the tree (setup 2) are seen striking in shots taken about 0.1 s apart (359:
  the bottom-left one out). On screen TL = pump1 (hose box4), BL = pump2 (box3),
  TR = pump3 (box2), BR = pump4 (box1); along the rails from the push end the
  barrow meets box1 (t 0.75-0.85), box2 (1.15-1.26), box3 (1.52-1.63), box4
  (1.82-1.95). By taps: onto box3 (pump2 stops), then off it timed from pump1's
  strike: pulling off at 0.47 s before it, or pushing off at about 0.65 s after
  it (the push starts after its 750 ms wind-up) gives pump2 pump1's beat.
  **The left pair is set** (pump1 = pump2, 44.59/44.72 and 46.84/46.84 in the
  log of the run); the barrow then went on towards box2. Save 94.
  Not yet sure: TL and TR have struck together in every reading since, through
  several pushes and pulls that should have crossed box2; either those crossings
  kept landing on pump1's beat or my TL region shows TR's strike (the tree
  shakes). Check first (see "Resume here").

- **tr, third session (15 Nov 2026), from save 94.** Which piston is which,
  settled by an observer run of a save made on the way (save 95: beats pump1 4,
  pump2 4, pump3 1, pump4 2) and by parking: on box2 the top-right piston stops
  for a whole cycle. So TL = pump1, BL = pump2, TR = pump3, BR = pump4, as the
  game's tree.cos chores name them (tr.hose_boxN = pumps 4..1). The barrow's own
  point is on box2 between -0.169 and -0.051 along the track from where it
  stood at save 95 (the hose strips from tr.set, crossed with Manny's track). By
  taps: onto box2 (a pull of 0.11), then off it by a pull timed from TL's strike
  (`trial.py 430 225 2 24 0.45 TL`; pump4 strikes about 1.1-1.3 s after TL, and
  a pull leaves the hose some 0.35-0.5 s after the tap). The first try, at
  TL+0.73, left just after BR struck (pump3 took the next beat); the second, at
  TL+0.45, gave pump3 pump4's beat, and the game's go_abnormal ran at once: the
  tree synched (360). Save 96. A tap on the barrow let go (361); a tap on the
  control panel, the switch: off; Glottis climbs the tree (362-365); the switch
  again: Glottis flung, the Bone Wagon gets its pogo sticks (366-368), back at
  the fork (369). Save 97.
- **sg, the sign** (fix 16). Manny got out of the Bone Wagon by a tap on it
  (371), a tap on the post: uprooted and held (373-374). The northwest trail
  (375-377): **na**, the clearing.
- **na, the sign.** Planted with a **two-finger tap on the floor, sign in hand**
  (question 1's binding: a held item used on nothing, here the sign's own use,
  which plants it), first at a guess: it points at a passageway (378-380, 390).
  Picked up by a tap, planted again. The spot is the game's
  `na.rubacava_point` (-1.22, -0.21), within 0.6 (16 px from above); its place
  on screen was read off the angle the game was really showing (na_intha:
  inventory.py's na_top projection was not the view, so the first aim missed;
  observer runs of saves 99 and 100 gave the sign's position). On the spot: the
  sign spins, the trapdoor opens (393-397). Save 101. A tap on the trapdoor:
  down to **lb**, the cave (398). A tap on the cave's sign: Manny reads the
  verse and takes the key (399-402). Save 102.

- **lb, na, sg (fourth session, 15 Nov 2026).** From save 102. The cave's way
  out: the first tap stops Manny at the game's own shortcut over the rocks
  (`lb_cheat1`/`lb_cheat2`, a walkOut that sets him at the far side, which ends
  the walk); a second tap on the way out carries on (411-412). Not a fault: the
  1998 keys stop there too. In na the sign's outline took floor taps (fix 18).
  Out by 'back' to sg (427). The Bone Wagon: a tap on it with the key still in
  hand (from the cave) is "use the Bone Wagon with the key", which does
  nothing; with the key put away (P, the coming swipe up), a tap gets Manny in
  (443). A tap on the bumpy road: over the rocks into **bv** (444-445).
  Save 107.
- **bv, bd: Busy Beavers.** A tap on the gate: "the way out of the forest", the
  flaming beaver chases Manny out (449-454). Save 108. Through the gate into
  **bd**; a tap on the dam (its outline, inside the bone heap's edge) takes a
  bone each time, P between (456-458). Save 109. The path down to the left: the
  tar angle (bd_rckws). **The beavers (moment 16):** a tap on the tar with a
  bone in hand: Manny throws it; when the pointer comes back, a tap on Manny
  (the coat), the left third until the extinguisher shows, the middle (take
  it), then **press and hold over the tar**: Manny sprays, and the beaver diving
  for the bone (about 10 s after the throw) freezes into the tar (497, 500,
  506). Three times (saves 112, 113, 114: all three dead, read in an observer
  run). The coat path is tight but plays: a player who misses throws another
  bone (the dam has plenty), as the walkthrough says. Bench helper:
  tools/proof/beaver.py (pointer steps only; it reads the screen for the
  pointer's return and the extinguisher's red, as the player looks).
  Two slips of mine, not faults: a P lost while a bone was held made the next
  dam tap "use bone on dam" (it goes back on the pile); and the coat reveal
  ignores a tap in its first second or two.
- **bv, the gate.** The padlock (the gate's left post): a tap, the key opens it;
  the Bone Wagon drives over the dam, out of the forest (512-515). The cut
  scenes to Rubacava's docks: Glottis's drag race, Meche (516-519). Manny at
  the foot of the lighthouse stairs (520-523). **Save 115.**
- Question 1's gesture (fix 17) wasn't needed in this stretch; the old two-finger
  binding is gone. Put away (P = the app's swipe up) was used before each dam
  tap, before the wagon, and before each throw.

### Year 1: Rubacava (fifth session, 15 Nov 2026)

- **re, ri: Welcome to Rubacava.** Up the stairs, into the diner; Celso by
  tapping lines ("What are you doing here?", "You must love her...", "How do
  you know your wife hasn't gone ahead...", "I'll help you find your wife...",
  "Well, I'd better go see how my other clients are doing"): the photo (531-
  537). Down the stairs, into the fog: rescued (540-546). Velasco: "Well, don't
  let me interrupt your car talk"; coat, the photo on him; "How do you know she
  sailed out of here?", "...car talk": the port log (547-555). Save 116. Up into
  the diner, the coat, the log on Celso; the cut scenes to Year 2 (558-565).
  Save 117.

### Year 2

- **cb, cf: Manny's office.** Out of the balcony into the office (567). The
  letters on the table: a tap reads them and takes them (575; the game's own use
  is lookAt, which picks them up first; a mouse.lua change made for it was not
  needed and was taken back). Save 120.
- **cc, ce, re, lm: the Lambada.** Down to the coat check; Lupe: "Okay, back to
  work" (586-587). Down the stairs to the docks: Meche, the cut scene (594-596).
  Save 121. **lm** (fix 19): Velasco: "Alright, I'm ready to sail!", "I'll
  work!", "...Glottis some tools...", "Who's the one guy...", "What if Naranja
  doesn't show up?", "So let me get this straight...", "I'd better go finish
  packing" (600-608). Save 122.
- **hb, bw, ev, ce, cc, ci: the union card.** Through the hub and the Blue
  Casket's elevator up to the cafe (610-623). The gold flake liqueur off the bar
  (625; P put it away). **cn**: Charlie: "Right. So what are you doing in it?",
  "How did you print fake betting stubs?", "What else can you counterfeit?",
  "Can you make reasonable union cards?": the VIP pass and the printer (629-
  634). Save 123. Stuck in the roulette room (fix 20), out (643). Save 125.
  The VIP pass on Glottis (649-650). Save 126.
- **ce, cl, ev, bw, dd, hb, xb: to the track.** The plaza, the elevator down,
  the dry dock, the hub, the extendo bridge (667). The lever: Manny pulls it, the
  bridge goes over (668-671; the first tap's pull ends while the bridge is still
  moving: wait for it). Across (672). Save 128.
- **tx, ts, kh, ks, tb, hh, hl, hk.** Up to the cat track; the plaque on the
  stuffed cat, by two fingers: Week 2 (679-681). The litter room: the can
  opener (685; the tap on the opener's outline took it, the shot shows the
  pickup). The betting hall, the lounge corridor, the VIP lounge (694). Save
  131. **hk**, the kitchen: the turkey baster (697). The waiter: he comes about
  every 20-27 s; the pantry closed by a tap (699); the scythe on the pantry doors
  while he is inside (712: the trap, "Oh! Zut!", 713). Save 133. The baster
  (715), the ladder, the can opener on the cask top (722-724); the stowaway (727-
  728). **wc**, the wine cellar (729). Save 134.
- **wc, de, dh: the forklift and the hidden floor** (moment 2, fix 21). On by a
  tap; into the elevator (731). Lined up on the lower lane, off by the seat,
  the button, back on, pushed at the window: jammed (757). Off, round to the
  lever side, a tap on the forklift: the forks up, the hidden hallway (765, 768).
  The suitcase (771-773); the union card's cut scene runs on (774-775). **Save
  146** (Manny with the suitcase, the hidden hall).

### Year 2: Seaman Naranja (seventh session, 15-16 Nov 2026)

- **tb, tw, ts, tx, xb, hb, bw, be, bi** (from save 146). Back through the
  betting hall, down to the dock, over the bridge, the hub, the Blue Casket
  (776-799). The microphone's outline took a floor tap (fix 22, 800-802). Save
  147. At the back, Lola and Olivia: the game quit (fix 23, 805-808); after it,
  Olivia: "Well, catch ya later, hep chick" (809-812). Save 148.
- **bk, the kitchen.** The coat, the baster, a tap on the sink: filled from the
  dishwater (813-820). P. Save 149.
- **xb, se: to Toto's.** The sea dock is reached from xb's track end: down the
  stairs to the pier (setup 3), then a tap at the dock end (565,320 on setup 4)
  walks Manny through the game's corridor into se (848). Not a fault: a tap
  by the lamp post lands in a sliver of floor beyond the corridor ("No path
  found"). Save 150. The hatch: down into **si** (849-851).
- **si: Naranja.** The back room. Fridge, crisper, the coat (the baster), a tap
  on the bottle: Manny waits for Toto to yell at the fridge and doses the
  bottle (857-870); Naranja drinks and drops (871-873). Save 152. A tap on the
  cot: the dog tags (877). P.
- **se, xb, tx, ts, tb, gt, sl: the blimp desk** (878-889). Save 153. The coat,
  the liqueur, a tap on Manny: he drinks; P. **A tap on the gate does not take
  him through** (the game's own sl.gate.use walks him 3 mm short of the
  detector's box; i1-i9, k3-k9; physical check P7); **a tap on the floor
  beyond it does** (341,239, inside detector_box): searched, the burp (m0-o7).
  Carla: "Hey, Carla, that's an awfully nice metal detector you have", "Yes"
  (902-904). Save 154.
- **ks: the litter box.** A tap on the treasure spot (342,392), the coat, the
  scythe, a tap on the litter in front: "Ah-ha!", the detector dug out (912-917,
  u1-u6). Save 156.
- **xb, hb, bw, dd, ev, pc, mg: the morgue.** The elevator tower is reached
  through the dry dock (dd's 'right'); its 'down' to the plaza (pc); the morgue
  door (pc setup 1). Save 157. The dog tags on corpse 1; the detector on
  Membrillo: Naranja is dead; the cut scenes (935-944). **Save 158** (Manny
  outside the morgue, pc).

## Resume here (after the seventh session, 16 Nov 2026)

- **Save 158** (build/bench/saves/grim158.gsv): Year 2, Seaman Naranja done,
  Manny outside the morgue in the plaza (pc). Start: `tools/proof/cycle.sh 158
  nosave`, then wait for the plain cursor. Steps: `tools/proof/g.py '<json>'`.
- Next (the walkthrough, Year 2 "SeaBee Tools"): Salvador's letter (Manny's
  office, cf) on the Blue Casket's beatniks, the book, the book on the bees;
  Nick in the VIP lounge: "Nick, I need a lawyer", "Friend of mine is in the
  slammer", "An excellent lawyer", "The very best is good enough for me", "You
  are, Nick"; again: "Virago, I REALLY need a lawyer", "I could tell Max about
  you and Olivia"; the cigarette case on Carla ("I don't know. I found it under
  your desk", "Yes"): the key; the lighthouse door, the card; the card on Lupe:
  the jacket; the jacket used on its own (a tap on Manny): the paper; the paper
  to Toto; the ticket printer: Week 2, Tuesday, Race 6, at the Photo Finish
  window; the photo on Nick. Then "Betting the Farm" (the roulette panel in
  Manny's office: the magnet when the right wheel's light is red) to the end of
  Year 2.
- Routes: the sea dock (Toto's) from xb's track end, down the pier stairs, then
  the dock end at 565,320; the elevator tower (morgue, plaza) via dd's 'right'.
- Physical checks: every timed or precise moment from here gets an entry in
  "Physical checks for Simon" and a save in build/for-simon (next slot 44).
- Held items: a tap on Manny uses it on its own; `{"key":"p"}` stands in for
  the swipe up (put away). The coat opens on the item last put away.
- Known ahead: the roulette panel (moment 12), the conveyor belt's invented
  `cy.offbelt` (Year 3), the lighthouse top.
- Bench notes: dialogue lines at x 90, rows y 396/418/439/461 (a two-line list
  sits at 439/461). Reading state: observer runs (`tools/proof/qq.sh <slot>
  <lua>`), never the proof game.
- The iOS libraries: `ScummVMKit/build-lib.sh sim|dev ./scummvm ./build-sim|dev`
  in ~/Developer/pointyclicky-build; the FreeType lines are in both config.mk
  (`INCLUDES += -I<deps>/include/freetype2`, `LIBS += -L<deps>/lib -lfreetype -lz
  -lbz2`); a reconfigure loses them.
- engine/grim_edition.patch is cut against ScummVM 2026.4.0 +
  grim_pointyclicky.patch alone (build/proof-bench/patchgen holds that base;
  the room adapter's grim.cpp/grim.h/module.mk changes are left out). This
  session: the old patch applied to a copy of the base, this session's two
  engine changes (hotspotman.cpp, gfx_tinygl.cpp) copied over, cut as a git
  diff in a scratch repo, and checked with `git apply --check` on a fresh copy.
