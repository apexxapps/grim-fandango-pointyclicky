# The proof playthrough (PLAN.md phase 5, item 2)

*Started 15 Nov 2026. **Done 16 Nov 2026: from a new game to the end credits**,
Years 1 to 4, by pointer only (shot 2038: the credits). Forty-three fixes on the
way; seventeen physical checks for Simon (build/for-simon, slots 36-52). What is
left is in "After the credits" at the end.*

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

24. **The union card at Velasco's: Manny stranded in the Blue Casket** (a dead
    end). Back at the Limbo dock with the union card, Velasco's check
    (lm.check_status) shows the card by `open_inventory(TRUE, TRUE)` and puts it
    back by `close_inventory()`, without ever showing the coat. Grim Mouse's
    close_inventory always runs Inventory.unload_inventory (its inCloseUpSet is
    forced TRUE), which mouse.lua had pointed at the coat's own return_to_set:
    so the closing went back to the set the coat was last opened in (the Blue
    Casket) and left Manny there, invisible, with the screen on the club and no
    way out (shots 975-979; read in an observer run of save 160: set bi, the
    check still running; the same at 984-987). mouse.lua: unload_inventory leaves
    the coat only when the coat is what's showing (the 1998 test); otherwise it
    keeps the button handler as it is. Proven from save 159: Velasco checks the
    card and Manny stays on the dock (990-996); save 160.
25. **Engine: a double tap beside Manny opened the coat** (hh, the lounge
    corridor, a near shot). Manny turns and steps into the spot between the two
    taps of a run, so the second was taken as a tap on him (1015). grim.cpp: the
    second tap of a double tap (within 500 ms and 24 px of the first, the first
    not on Manny) only makes the first a run. Proven: the same double tap runs
    (1022-1023). (Not a fix: a single tap on Manny's body still opens the coat.)
26. **The VIP lounge's door would not let Manny back in** (a dead end for
    Nick). The game reads a set afresh from its file each time Manny enters it,
    so a door's passage sectors go back to the file's "invisible" while the
    door's own `opened` stays TRUE from the last visit: Sentence("walkOut") sees it
    open and skips open(), and the walk through stops at the door (1026-1027;
    observer runs of saves 162 and 158: opened TRUE, the walk to the out point
    fails; with the passages made active it goes through). mouse.lua: after every
    set's enter (and after a load), each door the game holds open has its
    passages made active, as Object.open did. Proven from save 162: the door
    takes Manny into the lounge (1029); save 163.
27. **ev, setup 0 (the elevator station): the stairs walked Manny into the
    elevator.** The 'up' walk path went straight from wherever Manny stood to
    the stairs' top; from the elevator's door that crossed the elevator's box
    (be_box), so Manny rode down to the Blue Casket again (1116-1118; observer:
    he walked up the funnel into be_box). The path now goes by the floor's left,
    as 'up2' does (the walk sectors stairs_14, sect_6, stairs_15). In hand.txt.
    Proven: a single tap on the stairs from the elevator's door goes up to ce
    (1125-1128).
28. **Engine: Lupe could not be given the card** (cc, the coat check). Lupe is
    a character, found where she is drawn; behind the counter she is drawn
    mostly hidden by it, and her outline (the window) was dropped whenever she
    was live, so a tap on the window with the card walked instead (1143-1145,
    BENCH_DEBUG cc-dbg). hotspotman.cpp: a character's outline still takes taps
    while the character is drawn there (its screen box meets the outline); only
    once it has walked off its outline is the outline dropped. Proven from save
    168: the card on Lupe, the jacket (1146-1148). *Tools item:* the same held
    for every character drawn mostly behind something.
29. **The betting stub could not be used at the Photo Finish window** (a dead
    end). Grim Mouse's Object.rename (for its hover names) also replaced the
    object's string_name, which the game's Sentence uses to find a handler
    (use_<string_name>): the printed ticket was renamed "stub", so
    tb.photo_window.use_ticket never ran and the window did nothing (1219-1221;
    observer: "Executing sentence: use Window with stub", no handler). Two more
    were broken the same way: the Double-N ticket (me) and the fire
    extinguisher (tu: use_extinguisher). mouse.lua: rename keeps a string_name
    the game gave, and the three get theirs back (also in saves made before).
    Proven from save 172: the ticket goes through, the photo (1222-1225).
30. **cy, off the conveyor belt: Manny floated back to the anchor room every
    time** (a dead end for the chain: the belt has to be stepped off at its foot
    to work its lever). Coming up from the anchor room the belt is running down,
    and Manny has some 15 frames (half a second) on it before the belt carries
    him into its far end, where the game floats him back down ("Uh-oh"). The
    1998 way off is the game's jump box (cy.jump_box.walkOut: jump_off_conveyor,
    which stops the belt's pull itself); Grim Mouse's stand-in, cy.offbelt,
    first walked him to a point a metre up the belt, so the belt always won
    (observer runs of save 192: "Executing sentence: walkOut /cytx011/more belt"
    while the walk to the offbelt was still going; shots 1499-1505, the float
    back). mouse.lua: the offbelt now runs the jump at once (use_immediate, as
    walking into the jump box did), and it is touchable only while Manny is on
    the belt (the game makes the belt itself untouchable then; off it, the
    ground the offbelt's outline covers is plain floor again). Proven from save
    192: a tap on the floor beside the belt the moment Manny arrives, off (1506-
    1508); and twice more later, from the top of the belt (1570, 1597).
31. **Engine: the crane at the crusher end could not be moved off point 28**
    (ew, the crane cab). The crane as drawn (boom and all) covers the last
    points of its track, so every tap on the track near it was "on the crane"
    and lowered or raised it (1546-1551: four taps, Down, Up, Down, Up). Getting
    it lowered on the scoop's spot is the crane puzzle's own move, so it was
    workable only by luck. hotspotman.cpp `craneTap`: a tap within 14 px of
    another point of the track is a tap on the track, even over the crane; the
    log now names the point's place on screen. Proven: 28 to 27 and back
    (1553-1556), lowered at 28 by a tap on the crane above the track (1557).
32. **Engine: the broadaxe could not be dragged out of the vault's armour
    corner** (vo, setup 2; a dead end for the secret room). The broadaxe moment
    backs Manny to the floor point of a tap; in that camera the floor's last
    visible row is the camera's own boundary (vo_amrms), so no tap could back
    him out of the view, and the secret door is behind the camera (1652-1658:
    taps at the bottom of the screen ended "there" a few centimetres on).
    hotspotman.cpp: a tap within 10 px of the screen's edge is a point past
    it (the line from Manny through the tap, 0.6 on), and the drag ends when
    the game changes the camera; and "there" is now within 0.06 (it was 0.25,
    which made the drop on the tile, a 0.15-0.43 ring, a matter of luck). Proven
    from save 211: a tap at the bottom edge, out into the round room
    (1659-ax4); then back to the secret door and, in the secret room, onto the
    tile and away from it facing it, the drop: the tile breaks (1669-1679).

33. **my, setup 1 (the room under the tracks), the oil drums (mytx034).** The
    outline ran a strip over the whole floor along the bottom of the screen (0 to
    639, y 356-478), so with the rag in hand every tap on the floor down there
    was "tap on oil drum" and Manny walked back to the drums (1736-1737). Redrawn
    round the two drums (x 205-294, y 334-440); in hand.txt. Proven: the same tap
    walks (1739).
34. **Engine: a character's outline over another thing's** (xb, Year 4: Glottis
    by the garage doors). Glottis's outline in xb covers the whole track end with
    the garage doors inside it, and since fix 28 a character's outline takes taps
    while the character is drawn over it: every tap on the doors was "tap on
    Glottis" (1781-1783). hotspotman.cpp `outlineYields`: a tap outside the
    character's drawn box goes to any other object outlined there; only where
    nothing else is does the character's own outline take it (Lupe's window
    still works: nothing else is outlined there). Proven: "tap on doors" (1785).
35. **xb, Year 4: the garage doors did nothing** (a dead end: the way to the
    Bone Wagon and the gelatin). The doors are open (no out point), so the game's
    Sentence("walkOut") walks to their use point and wants Manny in the door's
    box (jb_door); the use point is 1.5 cm outside it, so every time "Didn't make
    it to the door's box" (1786; observer run of save 226). The 1998 player walked
    on into the box. mouse.lua `walk_and_do`: after a walkOut that leaves Manny
    outside an open door's box, a step 0.15 on from the use point the way the game
    faces him there, and if that puts him in the door's box, the door's own
    walkOut. Proven from save 226: into the garage (1787), and again later (1803).
36. **jb, setup 0, the dominos (jbtx056): the gelatin could not be frozen.**
    The outline was a sliver 35 x 8 px on the far side of the room; the dominos
    the game lays out (the floor sector sect_2, x 66-248 on screen) had none, so
    a tap on them with the liquid nitrogen walked, "No path found" (1805).
    Redrawn over the domino field as the game lays it; in hand.txt. Proven: the
    nitrogen on the dominos, the gelatin frozen (1806-1811).
37. **th, setup 0 (backstage), the coffee pot and the Thunder Boys.** The right
    Thunder Boy's outline covered the whole stage and the coffee pot's top, so a
    tap on the pot was "tap on Thunder Boy" (1833). Both Thunder Boys redrawn round
    themselves, the pot round the pot as drawn; in hand.txt. Proven: the pot taken
    (1835-1836).
38. **ly, setup 2 (the casino floor), the slot machine (lytx112).** A band over
    the whole floor (x 18-588), the gambler and Meche included, so a tap on the
    soldier in the trench coat was "tap on slot machine" (1859). Redrawn round the
    machine; in hand.txt. Proven: the soldier talks (1860).
39. **ly, the men's room and the service door: no way back to the basement.**
    Both doors are "/lytx120/door"; the outlines all had the first id, so the
    service door's outline on setup 1 and the only door outline on setup 6 were the
    men's room's, and from the men's room a tap on the way back out walked straight
    back in (1872-1874). The service door gets its own id (lytx120_1, the engine's
    name for the second) on setups 1 and 6, and each door its own outline on setup
    6; in hand.txt (with the men's room's setup 1 line, which a hotspots.py re-run
    otherwise doubles). Proven: through the service door to te (1876).
40. **at, setup 2 (the sewer tunnel), the Bone Wagon (attx003).** Its outline
    ran over the ladder and the whole floor to the catwalk, so once Manny was on
    the catwalk a tap on the way to the ladder was "tap on Bone Wagon": its use
    jumped him back on the wagon (1929). Redrawn round the wagon; in hand.txt.
    Proven from save 260: along the catwalk to the ladder (1930-1931).
41. **Engine: the coat could not be opened in the florist's doorway** (fi). The
    test that an outlined thing nearer the camera wins over Manny (fix 8) compared
    the door's point, half way up the door, with Manny's feet; from a camera above,
    the door's point is nearer the lens than his feet in front of it, so every tap
    on him was the door (1942-1943). hotspotman.cpp `tapOnManny`: Manny is taken
    at the thing's own height for that test. Proven: the coat (1944), the scythe
    on the ball of tape (1945).
42. **fp, setup 1, the florist's door (fptx005) and the left flowerbox
    (fptx004).** Only the door's right half was outlined; the flowerbox ran over
    the window and the door's left half, so a tap on the door was "tap on
    flowerbox" (1947). Both redrawn; in hand.txt. Proven: into the shop (1948).
43. **me, setup 0, Salvador in the back seat: no way to reach him.** He has no
    outline on this angle (the hotspot is on setup 5 only), and the car's outline
    covers him as drawn, so a tap on him was "tap on car" ("locked", 2003-2004).
    The car's outline has a notch where he is drawn, so the engine finds him as
    drawn (his actor is linked); in hand.txt. Proven: Salvador's goodbye
    (2014-2016).

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
    bridge), the dialogue rows (21 px apart, about 52 pt). Year 2's second half:
    the ticket printer's keys (about 42 x 36 px each, no time limit), Lupe's
    window, the lighthouse door from above (setup 1: the door is 33 x 58 px, and
    the doorway a tap must reach to walk in is smaller still: 1107-1108 took two
    taps), all fine.

P9. **The roulette panel's magnet (cf, Year 2, Betting the Farm).** Target: the
    magnet switch at the panel's top right (Grim Mouse's sxmagnet outline, 82 x
    65 px, about 205 x 160 pt): easy. Window: the panel's three lights take
    turns, one per table, about 42 s each (right, bottom, top left, so the
    right-hand one comes round every 2 minutes or so; measured on the bench, shots
    rl*); the switch must be thrown while the right-hand table's wheel still
    spins, which by the game's script (Roulette.spin_up: up in about 2 s, then
    slowing for about 13 s) is the first 15 s or so of its light. Thrown when the
    wheel has stopped it only buzzes (intrbuzz), and on another table it does
    nothing to Bogen. Gesture: tap the panel on the desk, wait for the light, tap
    the switch. Save 44 (proof save 175, the panel already open). OK: the bench
    threw it 1 s after the light came on (1269-1270). A person has to know which
    light is "the rightmost wheel" (the walkthrough's words) and wait up to two
    minutes; the hints should say "the right-hand light".

P10. **Chepito's pass (su, Year 3, the sunken Lola).** Target: Chepito as drawn
    as he walks past the dark edge of the light (about 60 x 130 px, about 150 x
    325 pt): easy. Window: he passes about once every 40 s and is on screen in
    the light for some 8 s; a tap on him then starts the talk (the moving
    Chepito object is touchable only while he's in the chepito_visible sector).
    The bench waited for his light (a brightness poll) and tapped 7.7 s after
    it rose (1331, 1340, 1348). Then the lantern: during his three bobs at the
    pearl (about 12 s after the line "Well, I don't wanna break your stride",
    for some 12 s) a tap on the lantern grabs him (1356-1360); and a tap on
    Glottis hands him over. Gesture: taps. Save 47 (proof save 180, before the
    walk to the edge). OK: a person sees him coming; a miss waits for the next
    pass. (On the bench the first two lantern tries missed by tapping too early,
    before the bait started; nothing is lost.)
P11. **Meche's ashtray (ar, Year 3).** Target: the ashtray (outline 105 x 62
    px, about 260 x 155 pt): easy. Window: Manny's twist of the ashtray has to
    come just before Meche's next idle is the ash flick (one of four idles,
    picked at random, each some 3-5 s); after it the ashtray goes back in
    about 2 s. The bench needed about 20 taps over several minutes (shots at*,
    au*, av*, aw*), at random moments; it is the 1998 puzzle as it was (the
    walkthrough: "this may take several tries"). A Meche talk opens if the tap
    lands on her outline, which overlaps the ashtray's left half (taps at
    345,355 kept opening it; at 305,350, the overlap's other side, the ashtray
    was taken every time). Gesture: tap the ashtray, again and again. Save 45
    (proof save 187). **Fiddly, and the 1998 game's own timing.** Suggested:
    nothing in the rule; the outline overlap could favour the ashtray when
    Manny is beside it (a hand fix), and the hints should say "keep twisting
    the ashtray until she flicks".
P12. **The vault door's tumblers (vd, Year 3).** Target: the wheel's halves on
    the close-up (big). Window: none, but precision: the four tumblers turn
    with the wheel while it's held (about 140 degrees a second, accelerating),
    each next one picked up when the one before passes its pin, and turning
    back resets the pins; all four must end between 248 and 290 degrees. The
    bench read the tumblers in observer runs to plan the holds (right 0.5 s, 2
    s, 3 s, 0.5 s; left 9 s, 1.7 s, 0.75 s; right 0.75 s), shots 1617-1626; a
    person reads them off the screen (the slots line up). Gesture: press and
    hold on a half, lift to stop. Save 46 (proof save 204). **Likely fiddly:**
    the hold is the 1998 key held, so the finger's lift is the stop; a hold
    accurate to a tenth of a second is needed at the end. Suggested: none in
    the rule; maybe a short tap could be a single small step (as the undrilled
    door's 45-degree turn is) once the door is drilled. For Simon.
P13. **The broadaxe drop on the tile (vi, Year 3).** Target: Manny has to stand
    0.15-0.43 from the tile (-0.236, -0.388) facing it within 30 degrees, then
    drop the axe (drop_test). By pointer: back onto the tile (a tap on it),
    then back away from it (a tap 0.35 off, so his back is to that point and
    his face to the tile), then a tap on Manny drops it (1673-1679). A tap that
    lands on Manny's own outline drops the axe at once (1674: the axe fell in
    the wrong place, picked up again). Gesture: taps on the floor, then on
    Manny. Save 48 (proof save 214, in the secret room with the axe). OK but
    unmarked: the tile is the one the water drained through; a person has to
    work out "stand back from it, facing it". Fine as the 1998 puzzle.

P14. **Charlie and the soldier (ly, Year 4, the casino).** Target: the soldier
    in the trench coat (setup 2: about 190 x 210 px, after fix 38): easy. Window:
    after the sheet on Charlie he leaves the table for the men's room and is back
    after some seconds; the soldier has to be talked to before that ("then quickly
    talk to the soldier"). The bench tapped him some 10 s after the sheet went on
    Charlie (1864-1869). Gesture: the coat, the sheet, tap Charlie; tap the soldier. Save
    49 (proof save 245). OK.
P15. **The elevator demon's question (ly, Year 4).** Target: a floor in the
    elevator's scrolling list (rows 21 px apart, about 52 pt). Window: none, but
    the answer is the last number up on the keno board, which changes; read it off
    the board on the way in. The bench read it (14) and scrolled the list by its
    last row and the row above (1955-1958). Gesture: taps on the list. Save 50
    (proof save 269). OK; the list's way back up is unmarked (moments.md 23).
P16. **The sewergator (at, Year 4).** Targets: the Bone Wagon (raised by the
    remote) driven up to the catwalk (the game stops it at the right place, "close
    enough"), the catwalk, the ladder, then the remote used on its own while the
    gator has turned towards Manny. Window: the gator turns while Manny is on the
    ladder; the remote then drops the wagon on its tail. The bench did it at the
    first try (1921-1935). Gesture: taps on the tunnel and the wagon (moment 5),
    the catwalk, the ladder, the coat, the remote, a tap on Manny. Save 51 (proof
    save 259). OK; a lot of steps, all of them the 1998 ones.
P17. **The ticket hunt behind the greenhouse (me, Year 4).** Target: Salvador's
    body behind the greenhouse, which the ticket in Manny's hand pulls towards
    within about 3 units and flies to within 0.5. Window: none. From the car the
    camera is far (setup 0): Manny is some 5 px tall on the hill, and taps on the
    way up landed short twice (2019-2024); behind the greenhouse (setup 5) it is
    easy. Gesture: taps on the floor, then the body. Save 52 (proof save 290).
    **Fiddly on the far camera**, fine once round the back. Suggested: none in the
    rule; the hints should say "round the back of the greenhouse".

(Also met, not timed: the porthole anchor (dp) can't be hooked while Manny is
still walking in, about 7 s after entering: a tap then says nothing and does
nothing (1294, 1305-1308); waited for, it hooks at once (dph). And at the
octopus (lu) the first tap with the scythe did nothing visible; the next, from
a save just after, worked (1688-1695). Neither stops the game.)

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

### Year 2: SeaBee Tools and Betting the Farm (eighth session, 16 Nov 2026)

- **pc, ev, bw, be, bi: the beatniks** (from save 158, 945-949). The coat, the
  letters, a tap on the revolutionaries: Salvador's letter read out (950-956);
  the book (957). **dd**: the book on the dock workers, Terry reads it, the
  strike (968-971). Save 159.
- **hb, lm: Velasco and the union card** (fix 24: stranded in the Blue Casket,
  975-979; after it, the check plays on the dock, 990-996). Save 160.
- **xb, tx, ts, kh, ks, tb, hh, hl: Nick.** The lounge corridor's double tap
  (fix 25, 1015, 1022-1023); the lounge door (fix 26, 1026-1029). Save 163. Nick:
  "Nick, I need a lawyer", "Friend of mine is in the slammer", "An excellent
  lawyer", "The very best is good enough for me", "You are, Nick"; again:
  "Virago, I REALLY need a lawyer", "I could tell Max about you and Olivia"
  (1031-1047). The cigarette case off his table (1049). P. Save 164.
- **tb, tw, gt, sl: the key.** Up to the blimp desk (1056-1069). The coat, the
  cigarette case, a tap on Carla: "I don't know. I found it under your desk",
  "Yes": the key (1070-1079). P. Save 165.
- **dd, lx: the lighthouse.** Down the dock past the strike (1088-1092); the
  door from the near view walks to "No path found" (the door's walk is off the
  floor from there), from above (setup 1) the key on the door (1093-1106), the
  doorway (two taps: 1107-1108), Lola's scene, the card (1109-1110). Save 166.
- **ev, ce, cc: Lupe.** The stairs from the elevator (fix 27, 1116-1128); the
  coat check, the card on Lupe (fix 28, 1143-1148): the jacket; a tap on Manny
  with the jacket (used on its own): the paper (1150-1152). Save 169. (Leaving cc
  just after, the game printed a Lua error from Lupe's idle script,
  _actors.lua's new_run_idle, "unexpected type to index table" (1153); the game
  went on, nothing lost: the 1998 script's own, not the edition's.)
- **ev, bw, hb, xb, se, si: Toto.** The paper on Toto (1173-1178). Save 170.
- **xb, tx, ts, tb: the photo finish.** The ticket printer used on its own (a tap
  on Manny with it in hand): week 2 (03 down to 02 by two taps), TUE, race 6,
  print (1201-1213). Save 171. The Photo Finish window from the floor at the
  bottom left (1218); the ticket on it (fix 29, 1219-1221; after it, 1222-1225):
  the photo. Save 173.
- **hh, hl: Nick's lawyer.** The photo on Nick (1235-1250); the cut scenes:
  Terry out (1251-1252). Save 174.
- **pc, ev, ce, cc, cf: Betting the Farm.** Up to the office (1253-1265); the
  panel on the desk (1266). Save 175 (physical check P9, slot 44). The right-hand
  light, the magnet switch: Bogen's table, the raid on the cafe (1269-1272).
  **End of Year 2.** Year 3 begins: the Bone Wagon ship, Salvador's message
  (1273-1274). **Save 176** (Manny on the ship's deck, lz).

### Year 3 (ninth session, 16 Nov 2026)

- **lz, il, ei: the ship.** The hatch, the ladder, down the hall: Glottis's
  rescue (1275-1282). The starboard anchor's button (raised), the controls: the
  left lever (starboard), let go, the button twice (lowered, raised: hooked)
  (1283-1291). **dp**: the coat, the scythe, the anchor; the first taps came
  while the game was still walking Manny in and did nothing (1294-1308; see
  the note under the physical checks); then hooked through the porthole (dph,
  1311). Back, P, the port anchor's button: the ship tears (1312-1316); the
  controls, the console below the levers (back): the ship splits (1317-1324).
  Save 180.
- **su: under the sea.** To the dark edge; Chepito's pass, tapped as he went by
  (P10, 1331), "Well, I don't wanna break your stride"; twice more before the
  lantern was tapped during the bait, not before it (1340-1355; save 181 at the
  choice); the lantern grabbed, Glottis tapped: Chepito handed over (1356-1364).
  Save 182. **ps**: up the ridge, round the rock in front: Chepito caught by the
  barnacle, the sub taken (1368-1385). Save 184.
- **fh, vd, ar, fo: the Edge of the World.** The doors, the elevator, the
  walkway to the right: Meche and Domino (1386-1404). Save 185. The angelitos:
  "Why do you want to bite me?", "What are you two doing in this cage?",
  "Listen, children...", "I'm here to help you get out of this cage", "My hands
  are not too big...", "...tiny tools", "Okay, back to work" (1408-1415); the
  hammer (1418-1419). Save 186. **ar**: the ashtray, twisted until Meche's ash
  flick: the stockings (P11, many tries; 1424-1438). Save 188.
- **ea, mn: Chepito.** The elevator down, left at the bottom: Chepito; the
  hammer on him: the Bust-All; the stockings on him: the gun (1442-1483). Save
  189.
- **cy, ac, cv, ew, cu, bu: the boat.** The belt's lever, onto the belt: up and
  over into ac, the anchor room (the belt was set to carry down); crawled back to
  cy and off the belt only after fix 30 (1489-1508). Save 193. The lever (up),
  the belt, cv, the ladder, the crane: over to the crusher end and lowered
  (1509-1529). **cu, bu**: down to the beach, the Bust-All on the scoop: the
  chain broken (1530-1538). Save 196. Back up the ramp, the crane: raised,
  lowered and raised at the crusher (fix 31, 1546-1563): the crusher freed;
  back to the conveyor end, lowered: the chain on the belt (1564-1567). Save
  199. Down, off the belt, the lever (the chain jams, bunches), again, again
  (1570-1580); up, the crane: raised (the chain pulled through: Poseidon)
  (1581-1590). Save 202.
- **vd, ar, dr, vo, vi: rescuing Meche.** Back to the ashtray room; the gun on
  Meche (1599-1607). Save 203. The vault door: the Bust-All on the jamb
  (1612-1616); the wheel, the tumblers lined up (P12, 1617-1626; save 205); the
  scythe in them, the handle: open (1627-1633). Save 207. In; the vault door
  closed; the scythe on the metal tab: the secret door (1634-1641). Save 208.
  The sprinkler (scythe), the valve (1642-1648). Save 209. The broadaxe from
  the armour corner (fix 32, 1649-1663), dragged to the secret room
  (1669-1672), onto the tile and away facing it, dropped: the tile breaks (P13,
  1673-1679). Save 215.
- **lu: Domino's fall.** The escape, Domino in the sub; the coat, the scythe, a
  tap on the octopus (the first did nothing visible; again from save 217:
  1692-1695): Domino's end. **End of Year 3.** Year 4 begins at the Petrified
  Forest's edge, the Number Nine (1696-1698). **Save 218.**

### Year 4 (tenth session, 16 Nov 2026)

- **tg, td, bs, my: saving Glottis** (from save 218). Down to the trucks, the
  coffin: Bruno, the mug (1699-1704). P. Up the tower: the Hell Train, the Gate
  Keeper's note (1705-1714). P. Under the tracks: Glottis: "What can I get you?",
  "Can't we make a new hot rod?" (1716-1725). Save 219. **mk**: the mug on the
  rack, the drawer twice: the rag (1726-1732). **my**: the rag on the oil drum
  (fix 33, 1736-1739). **mk**: the rag on the toaster: the fire, the mechanics,
  the mug's rocket flight (1740-1744); Glottis fuelled, the drive to Rubacava
  (1745-1747). Save 222.
- **xb, hb, lm, bw, be, bi, bk: the Bone Wagon.** The hub, the Limbo dock:
  Velasco, the bottle (1749-1755). The Blue Casket's kitchen: the bottle on the
  keg (1757-1765). Save 223. Back to Glottis with the gelatin; his talk (1766-
  1780). Save 224. The garage doors (fixes 34, 35; 1781-1787). Save 227. **se,
  si**: Toto's cabinet: the liquid nitrogen (1788-1797). Save 229. **jb**: the
  nitrogen on the dominos (fix 36, 1803-1811). Save 232. The dynamite: the Bone
  Wagon out, the escape (1812-1816). **End of Rubacava.**
- **lw, nq: the new headquarters.** The arm off the soldier's remains (1818-
  1819); Meche (1820-1821). Save 235.
- **sh, te, th, dr: the disguise.** Up the ladders to backstage (1824-1832). Save
  236. The coffee pot (fix 37, 1833-1836); up the ladder, the coffee on the
  Thunder Boys (1837-1841). Save 240. Down, the pot back on the burner (1842-1843);
  the dressing room: the makeup (1844-1845). Save 241. Up again, the arm on the
  snow machine's grinder, the grinder taken (1846-1852). Save 242.
- **ly: the soldier, Meche and Charlie.** The soldier twice (fix 38, 1856-1861);
  Meche twice: the sheet (1862-1863). Save 245 (P14, slot 49). The sheet on
  Charlie, the soldier at once: Charlie lured off (1864-1869). Save 246. The men's
  room: the disguise (1870-1871). Save 247. The way back (fix 39, 1872-1876).
- **nq: the gun from Bowlsley.** The photo from the wastebasket (1882-1883); the
  note, then the photo on the pigeon (1884-1891); Bowlsley's flight (1892-1893).
  Save 252. **lw, sh**: the remote (1894-1897). Save 253.
- **sh, zw, at: the sewergator.** The wagon raised and lowered (the remote used
  on its own), the grinder: the bone trail starts (1901-1910). Save 256. Down the
  trail through zw, grinding (1911-1916). Save 257. At its end: the gator's tunnel
  (1917-1920). Save 258. The tunnel ride: the remote (raised), up to the catwalk
  (1921-1926). Save 259 (P16, slot 51). On the catwalk (1927-1928); to the ladder
  (fix 40, 1929-1931), up a little, the remote: the tail pinned (1932-1935). Save
  263. Down, out to **fp** (1936-1939). Save 264.
- **fp, fi: the florist's.** In: Bowlsley hides (1940-1941); the coat in the
  doorway (fix 41, 1942-1944), the scythe on the ball of tape: the store wrecked
  (1945). Save 266. Back in (fix 42, 1946-1948): the gun and the ammo; out to sh
  (1949). Save 268.
- **te, ly, hf: meeting Hector.** Up to the casino floor (1950-1952). Save 269
  (P15, slot 50). The elevator demon, 14 off the keno board (1953-1958). Save 271.
  **hf**: Celso: "Actually, I work for Hector...", "The real question is...",
  "What exactly are you saving your money for?", "Well, enough about you guys...",
  "I just got back from the worst vacation..." (1960-1966); the cut scenes:
  Hector's office, the tickets (1967-1970). Save 272.
- **nl: Lady Luck.** On the ledge (1971-1975). The coat, the grinder on the
  gargoyle; the coat, the Sproutella on it: the sign drops (1976-1987). Save 278.
  The ladder: across, the tickets, Meche, the cut scenes to the meadow (1988-1989).
  Save 279.
- **me, mf: the final showdown.** The greenhouse door: Hector, shot (1990-1993);
  the meadow: the grinder on the wound ("Eeeeh!"), the liquid nitrogen on it: the
  poison stopped (1994-2001). Save 282. Salvador in the back seat (fix 43,
  2003-2016). Save 289. The suitcase: the ticket hops to his flowers; the ticket
  off them (2017-2018). Save 290 (P17, slot 52). Up the hill and round behind the
  greenhouse; the ticket flies to Salvador's body; the body: the key (2019-2028).
  Save 293. The car with the key: the gun (2029-2030). Save 295. Down to the water
  tower, the gun on it: Hector's end (2031-2034). The greenhouse door (2035): the
  ending (2036-2037) and **the end credits (2038-2039)**.

## After the credits (the run done, 16 Nov 2026)

- **The bar is met:** a new game to the end credits on the bench, every step by
  tap, two-finger tap, double tap, press and hold, the coat by a tap on Manny,
  Skip for cut scenes only (no keys), developer mode off in the proof game.
  Bench stand-ins used: `{"key":"p"}` for the swipe up (put away), `{"key":"esc"}`
  for Skip and for closing the coat.
- **Last save:** build/bench/saves/grim297.gsv (Hector dying, before the
  greenhouse door). Saves 50-297 are the run's.
- **For Simon:** the physical checks P1-P17 (build/for-simon, slots 36-52, the
  README there); the items marked "likely too hard" or "fiddly" are P1, P4, P11,
  P12 and P17. Then phase 5 item 5: the sign-off on the phone.
- **Left from the plan:** phase 5 item 3 (coverage: every object the game made
  touchable reached by the pointer at least once) was not counted in this run;
  the audit at zero (item 1) is separate.
- Tools notes: tools/proof/notes.txt (one line per batch) and fixes.txt (one
  line per fix).
- The iOS libraries and engine/grim_edition.patch: as in the ninth session's
  notes (build-lib.sh, the FreeType lines in both config.mk, the shared tree's
  bladerunner_fixes.patch kept; the patch cut against ScummVM 2026.4.0 +
  grim_pointyclicky.patch at build/proof-bench/patchgen, every file but
  hotspotman.cpp/h checked identical to the shared tree, checked with
  `git apply --check` on a fresh clone).
