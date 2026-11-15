# The proof playthrough (PLAN.md phase 5, item 2)

*Started 15 Nov 2026. In progress: Year 1, from a new game through El Marrow
to the Petrified Forest. Not yet at the credits.*

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

(NB `tools/hotspots.py` rewrites data/hotspots from the traces; a re-run must
keep these hand fixes, as it keeps the ones in outlines-review.md. Check
before re-running.)

---

## Questions for Simon

1. **Using a held item on Manny himself** (the mouthpiece, for the dental
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
